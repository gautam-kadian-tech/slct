"""Cron scripts module."""
from datetime import date, datetime, timedelta
from os import remove as os_remove

import pandas as pd
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import CharField, Count, OuterRef, Q, Subquery, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from accounts.models import (
    RoleNameFunctionType,
    TgtRlsRoleData,
    TrackingPageview,
    User,
    UserLoginDetail,
    UserRole,
    UserUrlScreenNameMapping,
)
from analytical_data.models import (
    CrmPricing,
    LpSchedulingPlantConstraints,
    PlantProductsMaster,
    TgtBridgingCost,
    ZoneMappingNew,
)
from analytical_data.utils.send_email import EmailService
from analytical_data.view_helpers import connect_db


def create_lp_scheduling_plant_constraints():
    """
    Method to create daily scheduling plant constraints objects at
    midnight.
    """
    # plant_grades = PlantProductsMaster.objects.all()
    # plant_constraint_objects = list()
    # for plant_grade in plant_grades:
    #     if plant_grade.variable_production_cost != 0:
    #         plant_constraint_objects.append(
    #             LpSchedulingPlantConstraints(
    #                 plant_id=plant_grade.plant_id,
    #                 grade=plant_grade.grade,
    #                 capacity=0,
    #                 date=timezone.now() + timedelta(days=3),
    #             )
    #         )
    # LpSchedulingPlantConstraints.objects.bulk_create(plant_constraint_objects)
    plant_grades = PlantProductsMaster.objects.all()
    plant_constraint_objects = list()
    for plant_grade in plant_grades:
        if plant_grade.variable_production_cost != 0:
            capacity = 0
            third_day_obj = LpSchedulingPlantConstraints.objects.filter(
                plant_id=plant_grade.plant_id,
                grade=plant_grade.grade,
                date=timezone.now() + timedelta(days=2),
            )
            if not third_day_obj:
                day_after_next_obj = LpSchedulingPlantConstraints.objects.filter(
                    plant_id=plant_grade.plant_id,
                    grade=plant_grade.grade,
                    date=timezone.now() + timedelta(days=1),
                )
                if day_after_next_obj:
                    day_after_next_obj = day_after_next_obj.first()
                    capacity = day_after_next_obj.capacity
                plant_constraint_objects.append(
                    LpSchedulingPlantConstraints(
                        plant_id=plant_grade.plant_id,
                        grade=plant_grade.grade,
                        capacity=capacity,
                        date=timezone.now() + timedelta(days=2),
                    )
                )
    LpSchedulingPlantConstraints.objects.bulk_create(plant_constraint_objects)


def change_status_tgt_bridging_cost():
    """
    Method to deactivate bridging cost data, update active_flag to
    false.
    """
    TgtBridgingCost.objects.filter(
        effective_end_date__lt=datetime.now(), active_flag=1
    ).update(active_flag=0)
    TgtBridgingCost.objects.filter(
        effective_end_date__isnull=True, active_flag=0
    ).update(active_flag=1)


# def save_crm_pricing_data():
#     raw_query = f"""
#     SELECT
#         "CRM_MARKET_MAPPING_PRICING"."DISTRICT" AS "district",
#         "CRM_MARKET_MAPPING_PRICING"."BRAND" AS "brand",
#         "CRM_MARKET_MAPPING_PRICING"."PRODUCT" AS "product",
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date AS "date",
#         MODE() WITHIN GROUP (
#             ORDER BY
#                 "CRM_MARKET_MAPPING_PRICING"."WHOLE_SALE_PRICE" DESC
#         ) AS "wsp_price",
#         MODE() WITHIN GROUP (
#             ORDER BY
#                 "CRM_MARKET_MAPPING_PRICING"."RETAIL_SALE_PRICE" DESC
#         ) AS "rsp_price"
#     FROM
#         "etl_zone"."CRM_MARKET_MAPPING_PRICING"
#     WHERE
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date = '{str(date.today())}'
#         AND "WHOLE_SALE_PRICE" > 0
#     GROUP BY
#         "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
#         "CRM_MARKET_MAPPING_PRICING"."BRAND",
#         "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date
#     ORDER BY
#         "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
#         "CRM_MARKET_MAPPING_PRICING"."BRAND",
#         "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date;
#     """
#     data = pd.read_sql(raw_query, connect_db())

#     if data.empty:
#         return

#     crm_pricing_query = Q()
#     for index, row in data.iterrows():
#         crm_pricing_query |= Q(
#             district=row["district"],
#             date=row["date"],
#             brand=row["brand"],
#             product=row["product"],
#         )

#     queryset = CrmPricing.objects.filter(crm_pricing_query).order_by(
#         "district", "brand", "product", "date"
#     )

#     objects_updated = []
#     for index, instance in enumerate(queryset):
#         for attr, value in data[index]:
#             setattr(instance, attr, value)
#         objects_updated.append(instance)
#     CrmPricing.objects.bulk_update(objects_updated, fields=["wsp_price", "rsp_price"])

#     objects_created = []
#     user_id = User.objects.first().id
#     for index, row in data[len(queryset) :].iterrows():
#         objects_created.append(
#             CrmPricing(
#                 **row,
#                 created_by=user_id,
#                 last_updated_by=user_id,
#                 last_update_login=user_id,
#             )
#         )
#     CrmPricing.objects.bulk_create(objects_created)


def save_crm_pricing_data():
    # raw_query = f"""
    #         SELECT
    #             "CRM_MARKET_MAPPING_PRICING"."DISTRICT" AS "district",
    #             "CRM_MARKET_MAPPING_PRICING"."BRAND" AS "brand",
    #             "CRM_MARKET_MAPPING_PRICING"."PRODUCT" AS "product",
    #             (
    #                 "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
    #             ) :: date AS "date",
    #             MODE() WITHIN GROUP (
    #                 ORDER BY
    #                     "CRM_MARKET_MAPPING_PRICING"."WHOLE_SALE_PRICE" DESC
    #             ) AS "wsp_price",
    #             MODE() WITHIN GROUP (
    #                 ORDER BY
    #                     "CRM_MARKET_MAPPING_PRICING"."RETAIL_SALE_PRICE" DESC
    #             ) AS "rsp_price"
    #         FROM
    #             "etl_zone"."CRM_MARKET_MAPPING_PRICING"
    #         WHERE
    #             (
    #                 "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
    #             ) :: date = '2023-08-26'
    #             AND "WHOLE_SALE_PRICE" > 0
    #         GROUP BY
    #             "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
    #             "CRM_MARKET_MAPPING_PRICING"."BRAND",
    #             "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
    #             (
    #                 "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
    #             ) :: date
    #         ORDER BY
    #             "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
    #             "CRM_MARKET_MAPPING_PRICING"."BRAND",
    #             "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
    #             (
    #                 "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
    #             ) :: date
    #             ;
    #         """
    raw_query = f"""
            SELECT
                district,
                brand,
                product,
                date,
                AVG(wsp_price) AS wsp_price,
                AVG(rsp_price) AS rsp_price
            FROM (
                SELECT
                    "CRM_MARKET_MAPPING_PRICING"."DISTRICT" AS "district",
                    "CRM_MARKET_MAPPING_PRICING"."BRAND" AS "brand",
                    "CRM_MARKET_MAPPING_PRICING"."PRODUCT" AS "product",
                    (
                        "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
                    ) :: date AS "date",
                    MODE() WITHIN GROUP (
                        ORDER BY
                            "CRM_MARKET_MAPPING_PRICING"."WHOLE_SALE_PRICE" DESC
                    ) AS "wsp_price",
                    MODE() WITHIN GROUP (
                        ORDER BY
                            "CRM_MARKET_MAPPING_PRICING"."RETAIL_SALE_PRICE" DESC
                    ) AS "rsp_price"
                FROM
                    "etl_zone"."CRM_MARKET_MAPPING_PRICING"
                WHERE
                    (
                        "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
                    ) :: date = '{str(date.today())}'
                    AND "WHOLE_SALE_PRICE" > 0
                GROUP BY
                    "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
                    "CRM_MARKET_MAPPING_PRICING"."BRAND",
                    "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
                    (
                        "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
                    ) :: date
            ) AS subquery
            GROUP BY
                district,
                brand,
                product,
                date
            ORDER BY
                district,
                brand,
                product,
                date;
        """

    data = pd.read_sql(raw_query, connect_db())

    if data.empty:
        # No need to proceed if there's no data
        exit()

    # Fetch the User object outside the loop
    user_id = User.objects.first().id

    # Prepare lists for bulk update and bulk insert
    records_to_update = []
    records_to_insert = []

    for index, row in data.iterrows():
        existing_records = CrmPricing.objects.filter(
            Q(district=row["district"])
            & Q(brand=row["brand"])
            & Q(product=row["product"])
            & Q(date=row["date"])
        )

        if existing_records.exists():
            # Update existing records
            existing_record = existing_records.first()
            existing_record.wsp_price = row["wsp_price"]
            existing_record.rsp_price = row["rsp_price"]
            records_to_update.append(existing_record)
        else:
            # Create new records
            new_record = CrmPricing(
                district=row["district"],
                brand=row["brand"],
                product=row["product"],
                date=row["date"],
                wsp_price=row["wsp_price"],
                rsp_price=row["rsp_price"],
                last_update_login=user_id,
                last_updated_by=user_id,
                created_by=user_id,
            )
            records_to_insert.append(new_record)
    # Perform bulk update and bulk insert operations within a transaction
    if records_to_update:
        CrmPricing.objects.bulk_update(
            records_to_update, fields=["wsp_price", "rsp_price"]
        )
    if records_to_insert:
        CrmPricing.objects.bulk_create(records_to_insert)


# def save_crm_pricing_data():
#     raw_query = f"""
#     SELECT
#         "CRM_MARKET_MAPPING_PRICING"."DISTRICT" AS "district",
#         "CRM_MARKET_MAPPING_PRICING"."BRAND" AS "brand",
#         "CRM_MARKET_MAPPING_PRICING"."PRODUCT" AS "product",
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date AS "date",
#         MODE() WITHIN GROUP (
#             ORDER BY
#                 "CRM_MARKET_MAPPING_PRICING"."WHOLE_SALE_PRICE" DESC
#         ) AS "wsp_price",
#         MODE() WITHIN GROUP (
#             ORDER BY
#                 "CRM_MARKET_MAPPING_PRICING"."RETAIL_SALE_PRICE" DESC
#         ) AS "rsp_price"
#     FROM
#         "etl_zone"."CRM_MARKET_MAPPING_PRICING"
#     WHERE
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date = '{str(date.today())}'
#         AND "WHOLE_SALE_PRICE" > 0
#     GROUP BY
#         "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
#         "CRM_MARKET_MAPPING_PRICING"."BRAND",
#         "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date
#     ORDER BY
#         "CRM_MARKET_MAPPING_PRICING"."DISTRICT",
#         "CRM_MARKET_MAPPING_PRICING"."BRAND",
#         "CRM_MARKET_MAPPING_PRICING"."PRODUCT",
#         (
#             "CRM_MARKET_MAPPING_PRICING"."COUNTER_VISIT_START_TIME" AT TIME ZONE 'UTC'
#         ) :: date;
#     """
#     data = pd.read_sql(raw_query, connect_db())

#     if data.empty:
#         return

#     crm_pricing_query = Q()
#     for index, row in data.iterrows():
#         crm_pricing_query |= Q(
#             district=row["district"],
#             date=row["date"],
#             brand=row["brand"],
#             product=row["product"],
#         )

#     queryset = CrmPricing.objects.filter(crm_pricing_query).order_by(
#         "district", "brand", "product", "date"
#     )

#     objects_updated = []
#     for index, instance in enumerate(queryset):
#         for attr, value in data[index]:
#             setattr(instance, attr, value)
#         objects_updated.append(instance)
#     CrmPricing.objects.bulk_update(objects_updated, fields=["wsp_price", "rsp_price"])

#     objects_created = []
#     user_id = User.objects.first().id
#     for index, row in data[len(queryset) :].iterrows():
#         objects_created.append(
#             CrmPricing(
#                 **row,
#                 created_by=user_id,
#                 last_updated_by=user_id,
#                 last_update_login=user_id,
#             )
#         )
#     CrmPricing.objects.bulk_create(objects_created)


def send_user_details():
    current_date = datetime.now()
    previous_date = current_date - timedelta(days=1)
    today = date.today()
    queryset = UserLoginDetail.objects.filter(
        date_time__date=previous_date, activity_type="Login"
    ).values(
        "id",
        "user",
        "activity_type",
        "date_time",
        "user__email",
        "user__name",
    )

    emails = [item["user__email"] for item in queryset]

    role_queryset = (
        UserRole.objects.filter(user__email__in=emails)
        .values("user_id", "user")
        .annotate(role_names=ArrayAgg("role_name"))
    )

    # Creating a dictionary mapping user_id to role_name
    user_id_to_role = {item["user_id"]: item["role_names"] for item in role_queryset}

    data_with_role = []
    # Adding 'role_name' to 'queryset' items based on 'user_id'
    for item in queryset:
        user_id = item["user"]
        role_name = user_id_to_role.get(user_id)
        if role_name is not None:
            item["role_name"] = role_name
            data_with_role.append(item)

    filename = f'data_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

    # Convert timezone-aware datetimes to timezone-unaware datetimes
    for row in data_with_role:
        # row["date_time"] += timedelta(hours=5, minutes=30)
        for field, value in row.items():
            if isinstance(value, datetime):
                if timezone.is_aware(value):
                    value = timezone.localtime(value)
                    value = timezone.make_naive(value)
                    row[field] = value

    df = pd.DataFrame(data_with_role)
    df.rename(
        columns={
            "id": "ID",
            "user": "USER",
            "user__name": "USER NAME",
            "user__email": "USER EMAIL",
            "role_name": "ROLE NAME",
            "activity_type": "ACTIVITY TYPE",
            "date_time": "DATE TIME",
        },
        inplace=True,
    )

    # Create an ExcelWriter object
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    # Write the first sheet to the Excel file
    df.to_excel(writer, sheet_name="user_details", index=False)

    page_tracking = pd.DataFrame(
        TrackingPageview.objects.filter(view_time__date=previous_date).values(
            "url", "visitor__user", "visitor__user__name", "visitor__user__email"
        )
    )

    if page_tracking.empty:
        page_tracking = pd.DataFrame(
            columns=[
                "url",
                "visitor__user",
                "visitor__user__name",
                "visitor__user__email",
            ]
        )
    screenwise_details = pd.DataFrame(
        UserUrlScreenNameMapping.objects.filter().values(
            "url", "screen_name", "persona", "page_action"
        )
    )

    merge_screen_df = pd.merge(page_tracking, screenwise_details, how="inner", on="url")
    merge_screen_df = merge_screen_df.drop_duplicates()
    merge_screen_df.drop(["url"], axis=1, inplace=True)
    merge_screen_df.rename(
        columns={
            "visitor__user": "USER",
            "visitor__user__name": "USER NAME",
            "visitor__user__email": "EMAIL",
            "screen_name": "SCREEN NAME",
            "persona": "PERSONA",
            "page_action": "PAGE ACTION",
        },
        inplace=True,
    )

    merge_screen_df.to_excel(writer, sheet_name="Screen_Name", index=False)

    personawise_count = (
        merge_screen_df.groupby(["USER", "USER NAME", "EMAIL", "PERSONA"])
        .size()
        .reset_index(name="personawise_user_count")
    )
    persona_counts_of_user = (
        personawise_count.groupby("PERSONA").size().reset_index(name="COUNT OF USERS")
    )

    persona_counts_of_user.to_excel(writer, sheet_name="Personawise_count", index=False)

    screenwise_count = (
        merge_screen_df.groupby(["USER", "USER NAME", "EMAIL", "SCREEN NAME"])
        .size()
        .reset_index(name="screenwise_count")
    )
    screen_counts_of_user = (
        screenwise_count.groupby(["USER", "USER NAME", "EMAIL"])
        .size()
        .reset_index(name="SCREEN COUNT")
    )

    page_action_count = (
        merge_screen_df.groupby(["USER", "USER NAME", "EMAIL", "PAGE ACTION"])
        .size()
        .reset_index(name="page_action_count")
    )
    action_counts_of_user = (
        page_action_count.groupby(["USER", "USER NAME", "EMAIL"])
        .size()
        .reset_index(name="ACTION COUNT")
    )

    merge_screen_action_df = pd.merge(
        screen_counts_of_user,
        action_counts_of_user,
        how="outer",
        on=["USER", "USER NAME", "EMAIL"],
    )
    merge_screen_action_df.to_excel(writer, sheet_name="Screen_Summary", index=False)

    # Save the ExcelWriter object to the file
    writer.save()

    EmailService.mail_with_attachments(
        "SLCT Daily Usage Report",
        f"Dear SLCT User,\n\nGreetings of the day!\n\nPlease find attached, yesterday's SLCT Usage Report for Production environment. The report indicates all the users who have accessed and used their screens and dashboards yesterday. You will find the user details, their roles and their login history in the attached report. \n \n This is a system generated email, kindly do not reply. For assisstance or queries, please reach out to local IT team.\n\nThank You\n\nKind Regards",
        [
            "anshul.mathur1@in.ey.com",
            "lakshya1@in.ey.com",
            "shivansh.gupta@in.ey.com",
            "rahul.oke@in.ey.com",
            "shikhir.gupta@in.ey.com",
            "vinayak.vipul@in.ey.com",
            "yash.sarda@shreecement.com",
            "aviral.suri@shreecement.com",
            "raunak.baid@shreecement.com",
            "kiran.mehrat@shreecement.com",
            "pavan.krishnaswamy@shreecement.com",
            "mahesh.pakalapati@shreecement.com",
            "sudhir.yadav@shreecement.com",
            "sukrit.joon@shreecement.com",
        ],
        attachments=filename,
    )
    # Close the ExcelWriter to release resources
    writer.close()
    os_remove(filename)


def user_adoption():
    current_date = datetime.now()
    previous_date = current_date - timedelta(days=1)
    last_7_days = current_date - timedelta(days=7)
    last_30_days = current_date - timedelta(days=30)
    financial_year_start = current_date.replace(month=4, day=1)

    user_role = pd.DataFrame(UserRole.objects.filter().values("role_name", "user_id"))
    rolename_function_type = pd.DataFrame(
        RoleNameFunctionType.objects.filter()
        .values("role_name", "function", "type")
        .distinct()
    )

    function_type_merging = pd.merge(
        user_role,
        rolename_function_type,
        on="role_name",
        how="outer",
    )

    user_login_dtl_yesterday = pd.DataFrame(
        UserLoginDetail.objects.filter(
            date_time__date=previous_date, activity_type="Login"
        ).values("user", "activity_type")
    )
    if user_login_dtl_yesterday.empty:
        user_login_dtl_yesterday = pd.DataFrame(
            columns=[
                "user",
                "activity_type",
            ]
        )
    user_login_dtl_yesterday = (
        user_login_dtl_yesterday.groupby("user").first().reset_index()
    )

    user_login_dtl_last_7_days = pd.DataFrame(
        UserLoginDetail.objects.filter(
            date_time__date__range=[last_7_days, previous_date], activity_type="Login"
        ).values("user", "activity_type")
    ).rename(columns={"user": "user_7", "activity_type": "activity_type_7"})

    user_login_dtl_last_7_days = (
        user_login_dtl_last_7_days.groupby("user_7").first().reset_index()
    )

    user_login_dtl_last_30_days = pd.DataFrame(
        UserLoginDetail.objects.filter(
            date_time__date__range=[last_30_days, previous_date], activity_type="Login"
        ).values("user", "activity_type")
    ).rename(columns={"user": "user_30", "activity_type": "activity_type_30"})

    user_login_dtl_last_30_days = (
        user_login_dtl_last_30_days.groupby("user_30").first().reset_index()
    )

    user_login_dtl_financial_year = pd.DataFrame(
        UserLoginDetail.objects.filter(
            date_time__date__range=[financial_year_start, previous_date],
            activity_type="Login",
        ).values("user", "activity_type")
    ).rename(columns={"user": "user_1_year", "activity_type": "activity_1_year"})

    user_login_dtl_financial_year = (
        user_login_dtl_financial_year.groupby("user_1_year").first().reset_index()
    )

    user_login_dtl_till_date = pd.DataFrame(
        UserLoginDetail.objects.filter(
            activity_type="Login",
        ).values("user", "activity_type")
    ).rename(columns={"user": "user_till_date", "activity_type": "activity_till_date"})

    user_login_dtl_till_date = (
        user_login_dtl_till_date.groupby("user_till_date").first().reset_index()
    )

    df_with_yesterday_dtl = pd.merge(
        function_type_merging,
        user_login_dtl_yesterday,
        left_on="user_id",
        right_on="user",
        how="outer",
    )

    df_with_7_day_dtl = pd.merge(
        df_with_yesterday_dtl,
        user_login_dtl_last_7_days,
        left_on="user_id",
        right_on="user_7",
        how="outer",
    )

    df_with_30_day_dtl = pd.merge(
        df_with_7_day_dtl,
        user_login_dtl_last_30_days,
        left_on="user_id",
        right_on="user_30",
        how="outer",
    )

    df_with_1_yr_dtl = pd.merge(
        df_with_30_day_dtl,
        user_login_dtl_financial_year,
        left_on="user_id",
        right_on="user_1_year",
        how="outer",
    )
    final_new_merging = pd.merge(
        df_with_1_yr_dtl,
        user_login_dtl_till_date,
        left_on="user_id",
        right_on="user_till_date",
        how="outer",
    )

    final_new_merging.drop(
        ["user", "user_7", "user_30", "user_1_year", "user_till_date"],
        axis=1,
        inplace=True,
    )

    final_new_merging = (
        final_new_merging.groupby(["role_name", "function", "type"])
        .count()
        .reset_index()
    )

    final_new_merging.rename(
        columns={
            "user_id": "total_users",
            "activity_till_date": "user_who_loggedin_TILL_DATE",
            "activity_type": "user_who_logged_in_yesterday",
            "activity_type_7": "user_who_logged_in_last_7",
            "activity_type_30": "user_who_logged_in_last_30",
            "activity_1_year": "user_who_logged_in_last_1_year",
        },
        inplace=True,
    )

    final_new_merging["Adoption_last_7_date"] = round(
        (
            final_new_merging["user_who_logged_in_last_7"]
            / final_new_merging["total_users"]
        )
        * 100,
        2,
    )
    final_new_merging["Adoption_last_7_date"] = final_new_merging[
        "Adoption_last_7_date"
    ].apply(lambda x: f"{x:.2f} %")

    final_new_merging["Adoption_last_30_date"] = round(
        (
            final_new_merging["user_who_logged_in_last_30"]
            / final_new_merging["total_users"]
        )
        * 100,
        2,
    )
    final_new_merging["Adoption_last_30_date"] = final_new_merging[
        "Adoption_last_30_date"
    ].apply(lambda x: f"{x:.2f} %")

    final_new_merging["Adoption_last_1_year"] = round(
        (
            final_new_merging["user_who_logged_in_last_1_year"]
            / final_new_merging["total_users"]
        )
        * 100,
        2,
    )
    final_new_merging["Adoption_last_1_year"] = final_new_merging[
        "Adoption_last_1_year"
    ].apply(lambda x: f"{x:.2f} %")

    final_new_merging["Adoption_till_date"] = round(
        (
            final_new_merging["user_who_loggedin_TILL_DATE"]
            / final_new_merging["total_users"]
        )
        * 100,
        2,
    )
    final_new_merging["Adoption_till_date"] = final_new_merging[
        "Adoption_till_date"
    ].apply(lambda x: f"{x:.2f} %")

    final_new_merging.rename(
        columns={
            "role_name": "ROLE NAME",
            "total_users": "TOTAL USER",
            "function": "FUNCTION",
            "type": "TYPE",
            "user_who_logged_in_yesterday": "USER WHO LOGGED IN YESTERDAY",
            "user_who_logged_in_last_7": "USER WHO LOGGED IN LAST 7 DAYS",
            "user_who_logged_in_last_30": "USER WHO LOGGED IN LAST 30 DAYS",
            "user_who_logged_in_last_1_year": "USER WHO LOGGED IN YTD",
            "user_who_loggedin_TILL_DATE": "USER WHO LOGGED IN TILL DATE",
            "Adoption_till_date": "ADOPTION TILL DATE",
            "Adoption_last_7_date": "ADOPTION LAST 7 DAYS",
            "Adoption_last_30_date": "ADOPTION LAST 30 DAYS",
            "Adoption_last_1_year": "ADOPTION YTD",
        },
        inplace=True,
    )
    final_new_merging = final_new_merging.sort_values(by=["TYPE"])

    filename = f'adoption_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

    # Create an ExcelWriter object
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    # Write the first sheet to the Excel file
    final_new_merging.to_excel(writer, sheet_name="Summary", index=False)

    overall_user_dtl = pd.DataFrame(
        UserRole.objects.filter()
        .values("role_name", "user__name", "user__email", "user__last_login")
        .distinct()
    ).rename(
        columns={
            "role_name": "ROLE",
            "user__name": "NAME",
            "user__email": "EMAIL",
            "user__last_login": "LAST LOGIN",
        }
    )

    overall_user_dtl["LAST LOGIN"] = overall_user_dtl["LAST LOGIN"].apply(
        lambda dt: dt.replace(tzinfo=None) if dt else dt
    )

    overalluser_to_function_type_merge = pd.merge(
        overall_user_dtl,
        rolename_function_type,
        left_on="ROLE",
        right_on="role_name",
        how="outer",
    )
    # overalluser_to_function_type_merge=overalluser_to_function_type_merge.drop_duplicates()
    # print(overalluser_to_function_type_merge)

    rls_role_data = pd.DataFrame(
        TgtRlsRoleData.objects.filter()
        .values("role", "name", "email", "zone", "state", "district")
        .distinct()
    ).rename(
        columns={
            "role": "ROLE",
            "name": "NAME",
            "email": "EMAIL",
        }
    )

    zone_mapping = ZoneMappingNew.objects.all().distinct()

    # Create a dictionary to map state to zone
    state_to_zone = {entry.state: entry.zone for entry in zone_mapping if entry.state}

    # Create a dictionary to map district to zone
    district_to_zone = {
        entry.district: entry.zone for entry in zone_mapping if entry.district
    }

    # Iterate over the rows of rls_role_data and update "zone" based on available information
    for index, data in rls_role_data.iterrows():
        if not pd.isna(data["zone"]):
            if not pd.isna(data["state"]) and data["state"] in state_to_zone:
                rls_role_data.at[index, "zone"] = state_to_zone[data["state"]]
            elif not pd.isna(data["district"]) and data["district"] in district_to_zone:
                rls_role_data.at[index, "zone"] = district_to_zone[data["district"]]

    rls_merge_df = pd.merge(
        overalluser_to_function_type_merge,
        rls_role_data,
        on=["ROLE", "NAME", "EMAIL"],
        # right_on=["ROLE", "NAME", "EMAIL"],
        how="left",
    )
    rls_merge_df.drop_duplicates(inplace=True)

    rls_merge_df.drop(
        ["role_name", "state", "district"],
        axis=1,
        inplace=True,
    )
    rls_merge_df.rename(
        columns={
            "function": "FUNCTION",
            "type": "TYPE",
            "zone": "ZONE",
        },
        inplace=True,
    )

    desired_order = ["ROLE", "NAME", "EMAIL", "FUNCTION", "TYPE", "ZONE", "LAST LOGIN"]

    # Rearrange the columns
    rls_merge_df = rls_merge_df[desired_order]

    rls_merge_df = rls_merge_df.sort_values(by=["TYPE"])

    # Replace Nan to None
    # rls_merge_df = rls_merge_df.where(pd.notnull(rls_merge_df), None)

    central_zone_df = (
        rls_merge_df[rls_merge_df["ZONE"] == "Central"]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    central_zone_df.to_excel(writer, sheet_name="Central_Zone_Details", index=False)

    east_zone_df = (
        rls_merge_df[rls_merge_df["ZONE"] == "East"]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    east_zone_df.to_excel(writer, sheet_name="East_Zone_Details", index=False)

    south_zone_df = (
        rls_merge_df[rls_merge_df["ZONE"] == "South"]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    south_zone_df.to_excel(writer, sheet_name="South_Zone_Details", index=False)

    north_zone_df = (
        rls_merge_df[rls_merge_df["ZONE"] == "North"]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    north_zone_df.to_excel(writer, sheet_name="North_Zone_Details", index=False)

    north1_zone_df = (
        rls_merge_df[rls_merge_df["ZONE"] == "North 1"]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    north1_zone_df.to_excel(writer, sheet_name="North1_Zone_Details", index=False)

    north2_zone_df = (
        rls_merge_df[rls_merge_df["ZONE"] == "North 2"]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    north2_zone_df.to_excel(writer, sheet_name="North2_Zone_Details", index=False)

    zone_list = ["Central", "East", "South", "North", "North 1", "North 2"]
    other_zone_df = (
        rls_merge_df[~rls_merge_df["ZONE"].isin(zone_list)]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    other_zone_df.to_excel(writer, sheet_name="Other_Zone_Details", index=False)

    # Save the ExcelWriter object to the file
    writer.save()

    EmailService.mail_with_attachments_adoption(
        "SLCT Adoption Report",
        f"Dear Users,\n\nGreetings of the day!\n\nPlease find the attached report on adoption of SLCT dashboards and screens. Adoption is based on numbers of users who have logged in atleast once vs total number of registered users. \n \n This is a system generated email, please do not reply. For any support reach out to your local IT team. \n\nThank You\n\nKind Regards",
        [
            "anshul.mathur1@in.ey.com",
            "lakshya1@in.ey.com",
            "shivansh.gupta@in.ey.com",
            "rahul.oke@in.ey.com",
            "shikhir.gupta@in.ey.com",
            "vinayak.vipul@in.ey.com",
            "yash.sarda@shreecement.com",
            "aviral.suri@shreecement.com",
            "raunak.baid@shreecement.com",
            "kiran.mehrat@shreecement.com",
            "pavan.krishnaswamy@shreecement.com",
            "mahesh.pakalapati@shreecement.com",
            "sudhir.yadav@shreecement.com",
            "sukrit.joon@shreecement.com",
        ],
        attachments=filename,
    )
    # Close the ExcelWriter to release resources
    writer.close()
    os_remove(filename)
