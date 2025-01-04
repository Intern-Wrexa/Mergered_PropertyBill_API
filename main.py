from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import httpx
import uvicorn

app = FastAPI()


# root function
@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                h1 {
                    font-size: 48px;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>Api Made By D</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# get property details for old bill
@app.get("/fetch-property-details/old-bill/load-response/")
async def fetch_property_details_old_bill(zone: str, ward: str, propertyId: str, subNo: str, rhtml: bool = False):
    url = f"https://erp.chennaicorporation.gov.in/ptis/citizensearch/searchPropByBillNumber!search.action?isNew=N&zoneNo={zone}&wardNo={ward}&propertyId={propertyId}&subNo={subNo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        if rhtml:
            # Return the raw HTML inside a response if rhtml is True
            return HTMLResponse(content=response.text)
        else:
            # Return the raw HTML inside a JSON object if rhtml is False
            return JSONResponse(content={"html": response.text})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch details")


# get property details for new bill
@app.get("/fetch-property-details/new-bill/load-response/")
async def fetch_property_details_new_bill(zone: str, ward: str, bill: str, rhtml: bool = False):
    url = f"https://erp.chennaicorporation.gov.in/ptis/citizensearch/searchPropByBillNumber!search.action?isNew=Y&newzoneNo={zone}&newwardNo={ward}&newbillNo={bill}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        if rhtml:
            return HTMLResponse(content=response.text)
        else:
            return JSONResponse(content={"html": response.text})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch details")


