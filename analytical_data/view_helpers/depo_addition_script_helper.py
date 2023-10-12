import time
import warnings
from datetime import datetime as dt

import numpy as np
import pandas as pd
import pulp as p
from geopy.distance import distance as calc_dist

warnings.filterwarnings("ignore")
from django.conf import settings

from .connection import connect_db


def lat_long_offset(lat, lon, x, y):
    """
    lat, lon : Provide lat lon coordinates
    x, y : Provide offset of x and y on lat and long respectively
           This needs to be in meters!

    The approximation is taken from an aviation formula from this stack exchange
    https://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """

    # Earth’s radius, sphere
    R = 6378137

    # Coordinate offsets in radians
    dLat = x / R
    dLon = y / (R * np.cos(np.pi * lat / 180))

    # OffsetPosition, decimal degrees
    latO = lat + dLat * 180 / np.pi
    lonO = lon + dLon * 180 / np.pi

    return latO, lonO


def get_mesh(lat, lon, dist, coors):
    # Create a vectorized offset function
    lat_long_offset_vec = np.vectorize(lat_long_offset)

    # calculate min and max range for coordinates over an axis
    mini, maxi = -dist * coors, dist * coors

    # calculate number of points over an axis
    n_coord = coors * 2 + 1

    # create an axis from min to max value with required number of coordinates
    axis = np.linspace(mini, maxi, n_coord)

    # create an "offset_grid" for X and Y values for both axis.
    X, Y = np.meshgrid(axis, axis)

    # calcualte offset coordinates for "offset_grid" in meters
    mesh = lat_long_offset_vec(lat, lon, X, Y)

    # Transpose to get the (x,y) values for the offset_grid's shape
    mesh_x_y_format = np.stack(mesh).transpose(1, 2, 0)
    return mesh_x_y_format


def get_existing_lead(cnxn):
    existing_lead = pd.read_sql(
        """
        select
        tosal."STATE",
        tosal."DISTRICT",
        tosal."TALUKA",
        round(avg(lm."DISTANCE"),1) as "EXISTING_DEPO_LEAD"
        from etl_zone."LINKS_MASTER" lm
        inner join (
        select * from etl_zone."T_OEBS_SCL_ADDRESS_LINK"
        where "ACTIVE" = 'Y'
        and "Active" = 1
        ) tosal on tosal."CITY_ID" = lm."TO_CITY_ID"
        where lm."PRIMARY_SECONDARY_ROUTE" = 'SECONDARY'
        group by tosal."STATE", tosal."DISTRICT", tosal."TALUKA"
        """,
        cnxn,
    )

    return existing_lead


def get_grid_coords(df):
    output = get_mesh(df.LAT_WT.mean(), df.LONG_WT.mean(), 10000, 200)

    grid_coords = pd.DataFrame(columns=["DEPOT_LAT", "DEPOT_LONG"])
    for coords in output:
        grid_coords = grid_coords.append(
            pd.DataFrame(columns=["DEPOT_LAT", "DEPOT_LONG"], data=coords),
            ignore_index=True,
        )
    grid_coords["JOIN"] = 1

    grid_coords = grid_coords.query(
        f"""
        DEPOT_LAT >= {df['LAT_WT'].min()-0.5}&DEPOT_LAT <= {df['LAT_WT'].max()+0.5}&DEPOT_LONG >= {df['LONG_WT'].min()-0.5}&DEPOT_LONG <= {df['LONG_WT'].max()+0.5}
    """
    )

    return grid_coords


def get_inputs(cnxn, brand):
    df_main = pd.read_csv(settings.DATA_ONE_CSV)
    df_main = df_main[df_main["BRAND"] == brand].reset_index(drop=True)

    sla_dist = pd.read_sql(
        """
        select
        "STATE"
        ,"DISTRICT"
        ,"TALUKA"
        ,"SECONDARY_PTPK"
        ,"PROMISED_MARKET_SLA"*25 as "SLA_DIST"
        from etl_zone."DEPOT_ADDITION_MASTER"
    """,
        cnxn,
    )

    return df_main, sla_dist


def get_taluka_centroids(df):
    df.set_index(["STATE", "DISTRICT", "TALUKA"], inplace=True)

    df["LAT_WT"] = df.groupby(df.index).apply(
        lambda x: np.average(x["LAT"], weights=x["COUNTER_POTENTIAL"])
    )
    df["LONG_WT"] = df.groupby(df.index).apply(
        lambda x: np.average(x["LONG"], weights=x["COUNTER_POTENTIAL"])
    )
    df["POTENTIAL"] = df.groupby(df.index).apply(
        lambda x: np.sum(x["COUNTER_POTENTIAL"])
    )

    df = (
        df.reset_index()[
            ["STATE", "DISTRICT", "TALUKA", "LAT_WT", "LONG_WT", "POTENTIAL"]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    df["JOIN"] = 1

    return df


def run_model(df, depot_cost, max_taluka_per_depot):
    start = time.time()
    # add variable names to dataframe

    df["CODE"] = df["STATE"] + "_" + df["DISTRICT"] + "_" + df["TALUKA"]

    df["index"] = df.index

    df["OBJECTIVE_FUNC"] = df["DISTANCE"] * df["SECONDARY_PTPK"] * df["POTENTIAL"]

    var_names = ["x" + str(i) for i in range(len(df))]
    df["variables"] = pd.Series(var_names)

    df["variables_depot_idx"] = df.groupby(
        ["DEPOT_LAT", "DEPOT_LONG"], as_index=False
    ).ngroup()
    df["variables_depot"] = "y" + df["variables_depot_idx"].astype("str")

    # 1. initialize problem
    # 2. declare Variables
    # 3. declare Objective Function
    # 4. set objective function in model
    lp_prob = p.LpProblem("Minimize_Distance", p.LpMinimize)
    var_names_model = [p.LpVariable(i, lowBound=0, cat="Binary") for i in var_names]
    var_names_depot = [
        p.LpVariable(i, lowBound=0, cat="Binary")
        for i in df["variables_depot"].unique().tolist()
    ]

    objective_func = df["OBJECTIVE_FUNC"].tolist()

    objective_list = [
        var_names_model[i] * objective_func[i] for i in range(len(var_names_model))
    ]
    objective_list1 = [
        var_names_depot[i] * depot_cost for i in range(len(var_names_depot))
    ]

    lp_prob += p.lpSum(objective_list) + p.lpSum(objective_list1)

    # Constraint 1 - Number of Depots

    for i in var_names_depot:
        val = df[df["variables_depot"] == str(i)]["index"].tolist()
        lp_prob += (
            p.lpSum([var_names_model[i] for i in val]) <= max_taluka_per_depot * i
        )

    # Constraint 2 - Every counter must be served

    counter_idx = df.groupby("CODE")["index"].apply(list)

    for idx, val in counter_idx.items():
        lp_prob += p.lpSum([var_names_model[i] for i in val]) == 1

    # solve problem
    status = lp_prob.solve()

    print("Status = ", p.LpStatus[status])
    print("TC = ", p.value(lp_prob.objective))

    var_out = {}
    for i in var_names_model:
        var_out[str(i)] = int(p.value(i))

    var_out1 = {}
    for i in var_names_depot:
        var_out1[str(i)] = int(p.value(i))

    df["IS_SERVED"] = df["variables"].apply(lambda x: var_out[x])
    df["IS_SERVED1"] = df["variables_depot"].apply(lambda x: var_out1[x])

    print("Time Taken", time.time() - start)

    df = df[df["IS_SERVED"] == 1].reset_index(drop=True)

    return df


class DepotAdditionRunHelper:
    def get_optimal_depots(brand, depot_cost, max_taluka_per_depot):
        cnxn = connect_db()

        df, sla_dist = get_inputs(cnxn, brand)

        df = get_taluka_centroids(df)

        grid_coords = get_grid_coords(df)

        df = df.merge(grid_coords, on=["JOIN"])

        df["DISTANCE"] = df.apply(
            lambda x: calc_dist((x.LAT_WT, x.LONG_WT), (x.DEPOT_LAT, x.DEPOT_LONG)).km,
            axis=1,
        )

        df = df.merge(sla_dist, on=["STATE", "DISTRICT", "TALUKA"])
        df = df[df["DISTANCE"] <= df["SLA_DIST"]].reset_index(drop=True)

        df = run_model(df, depot_cost, max_taluka_per_depot)

        df.rename(
            columns={
                "LAT_WT": "LAT",
                "LONG_WT": "LONG",
                "DISTANCE": "RECOMMENDED_DEPO_LEAD",
            },
            inplace=True,
        )

        df = df[
            [
                "STATE",
                "DISTRICT",
                "TALUKA",
                "LAT",
                "LONG",
                "POTENTIAL",
                "DEPOT_LAT",
                "DEPOT_LONG",
                "RECOMMENDED_DEPO_LEAD",
            ]
        ]
        existing_lead = get_existing_lead(cnxn)

        df = df.merge(existing_lead, on=["STATE", "DISTRICT", "TALUKA"], how="left")
        df["EXISTING_DEPO_LEAD"] = df["EXISTING_DEPO_LEAD"].fillna(0)
        return df


# if __name__ == '__main__':

#     cnxn = connect_db()

#     brand = 'SHREE'
#     depot_cost = 100000
#     max_taluka_per_depot = 10

#     output = get_optimal_depots(brand,depot_cost,max_taluka_per_depot)

#     print(output)

#     cnxn.close()
