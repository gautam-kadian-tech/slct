"""Transfer accounts views helper module."""
from analytical_data.models.non_trade_head_models import (
    NtAccRelation,
    DimResources,
    DimAccountType,
    DimCustomersTest,
)
import pandas as pd
import json
from background_task import background


class TransferAccountsHelper:
    """Transfer accounts views helper class."""

    @background(schedule=10)
    def background_create(user_id, comments, resource_id, transfer_from_id):
        """Creates a background task to manipulate customer account
        relations data and fire bulk create query.

        Args:
            data (dict): validated request data
            user_id (int): currently logged in user's id
        """
        queryset = NtAccRelation.objects.filter(resource__id=transfer_from_id)
        df = pd.DataFrame(list(queryset.values()))
        data = {
            "comments": comments,
            "resource": resource_id,
            "created_by": user_id,
            "last_updated_by": user_id,
            "last_update_login": user_id,
        }
        df["effective_till"] = df["effective_till"].astype(str)
        df = (
            df.assign(**data)
            .drop(
                columns=[
                    "resource_id",
                    "creation_date",
                    "last_update_date",
                    "effective_from",
                    "parent_id_id",
                ],
                axis=1,
            )
            .rename(
                columns={
                    "id": "parent_id",
                    "cust_id": "cust",
                    "account_type_id": "account_type",
                }
            )
        )
        transferred_accounts = list(
            map(
                lambda data: NtAccRelation(
                    resource=DimResources.objects.get(id=data.pop("resource")),
                    cust=DimCustomersTest.objects.get(id=data.pop("cust")),
                    account_type=DimAccountType.objects.get(
                        id=data.pop("account_type")
                    ),
                    parent_id=NtAccRelation.objects.get(id=data.pop("parent_id")),
                    **data,
                ),
                json.loads(df.to_json(orient="records")),
            )
        )
        NtAccRelation.objects.bulk_create(transferred_accounts)
