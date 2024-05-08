import pandas as pd
from .utils import room_division


class tracking:
    def __init__(self) -> None:
        pass

    def eval_od_matrix(self, df_t_1: pd.DataFrame, df_t: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate the OD matrix among two dataframes in two different time instant\n
        Input:
        - df_t_1: dataframe at time t-1
        - df_t: dataframe at time t\n
        Output:
        - OD_matr: the OD matrix
        """
        # df_t_1 = room_division(df_t_1)
        # df_t = room_division(df_t)

        df_t_1 = df_t_1.drop_duplicates("user_masked")
        df_t = df_t.drop_duplicates("user_masked")

        df_moved = df_t.merge(df_t_1, on=["user_masked"], how="inner", indicator=True)
        df_moved = df_moved.drop(
            ["name_ap_x", "name_ap_y", "APnum_x", "APnum_y", "_merge"], axis=1
        )
        OD_matr = (
            df_moved.assign(count=1)
            .pivot_table(
                index="Room_x", columns="Room_y", values="count", aggfunc="count"
            )
            .fillna(0)
        )
        return OD_matr
