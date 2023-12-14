import json

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build


class SpreadSheets:
    def __init__(self, credentials_file_path: str):
        self.credentials_file_path = credentials_file_path
        self.service = self.get_service()

    def get_credentials(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file_path,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        return credentials

    def get_values_dataframe(self, data_frame: pd.DataFrame) -> list:
        col_names = data_frame.columns.to_list()
        values = data_frame.to_json(orient="values", date_format="iso")
        values_list = json.loads(values)

        # Agregar col_names al principio de values_list
        values_list.insert(0, col_names)

        return values_list

    def get_service(self):
        service = build("sheets", "v4", credentials=self.get_credentials())
        return service

    def verify_sheet_existence(self, spreadsheet_id, sheet_name):
        service = self.service
        spreadsheet_info = (
            service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        )

        sheet_exists = any(
            sheet["properties"]["title"] == sheet_name
            for sheet in spreadsheet_info["sheets"]
        )
        return sheet_exists

    def clean_sheet(self, spreadsheet_id, worksheet_name):
        self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=worksheet_name,
        ).execute()

    def add_sheet(self, spreadsheet_id, worksheet_name):
        if self.verify_sheet_existence(spreadsheet_id, worksheet_name):
            return False

        service = self.service
        batch_update_values_request_body = {
            "requests": [{"addSheet": {"properties": {"title": worksheet_name}}}]
        }
        request = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=batch_update_values_request_body
        )
        response = request.execute()

        return True

    def append_dataframe(
        self, data_frame: pd.DataFrame, spreadsheet_id: str, worksheet_name: str
    ):
        service = self.service

        # Preparamos datos en formato para Google Sheets
        data = self.get_values_dataframe(data_frame)

        # Verificamos existencia de SpreadSheet
        sheet = self.add_sheet(spreadsheet_id, worksheet_name)

        # Si la hoja no existe entonces limpiamos la hoja
        if not sheet:
            self.clean_sheet(spreadsheet_id, worksheet_name)

        # Agregamos la data al Sheet
        response = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=worksheet_name,
                body={"values": data},
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
            )
            .execute()
        )

        return response

    def worksheet_to_dataframe(self, spreadsheet_id: str, worksheet_name: str):
        service = self.service

        # Agregamos la data al Sheet
        response = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=worksheet_name)
            .execute()
        )

        # Obtener los valores del rango
        values = response.get("values", [])

        if not values:
            print("No hay datos encontrados.")
            return None

        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(values[1:], columns=values[0])

        return df
