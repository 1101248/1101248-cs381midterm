import requests
import csv

# API endpoint（你可改為自己的實際網址）
API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWA-25D455AA-409A-4F4E-A61B-0C74D0ACC874"

def fetch_earthquake_data():
    try:
        response = requests.get(API_URL)
        data = response.json()

        earthquakes = data["records"]["Earthquake"]

        with open("api.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "地震編號", "報告類型", "時間", "震央", "緯度", "經度",
                "深度(km)", "規模", "最大震度", "報告內容", "圖片網址", "報告連結"
            ])

            for eq in earthquakes:
                eq_info = eq.get("EarthquakeInfo", {})
                epicenter = eq_info.get("Epicenter", {})
                magnitude = eq_info.get("EarthquakeMagnitude", {})

                writer.writerow([
                    eq.get("EarthquakeNo"),
                    eq.get("ReportType"),
                    eq_info.get("OriginTime"),
                    epicenter.get("Location"),
                    epicenter.get("EpicenterLatitude"),
                    epicenter.get("EpicenterLongitude"),
                    eq_info.get("FocalDepth"),
                    magnitude.get("MagnitudeValue"),
                    eq.get("ReportContent").split("最大震度")[-1].replace("。", "") if "最大震度" in eq.get("ReportContent", "") else "",
                    eq.get("ReportContent"),
                    eq.get("ReportImageURI"),
                    eq.get("Web")
                ])

        print("✅ 成功寫入 api.csv")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    fetch_earthquake_data()
