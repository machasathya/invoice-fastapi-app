from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, oauth2, util
from app.database import get_db
from datetime import datetime
from starlette.responses import PlainTextResponse
import platform
import subprocess
import tempfile

router = APIRouter()


@router.post("/invoice", response_model=schemas.InvoiceOut)
def add_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    items, quantities = util.create_invoice(invoice)
    result = util.calculate_invoice(items=items, quantities=quantities, invoice=invoice)

    # Convert string date to datetime
    date_obj = datetime.strptime(result["date"], "%d-%m-%Y %H:%M:%S")

    db_invoice = models.Invoice(
        customer_name=result["customer_name"],
        total_quantity=result["total_quantity"],
        total_amount=result["total_amount"],
        date=date_obj,
        unit_prices=invoice.unit_prices,
        rent=result["rent"],
        created_by=current_user.id
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return {
        "id": db_invoice.id,
        "customer_name": db_invoice.customer_name,
        "total_quantity": db_invoice.total_quantity,
        "total_amount": db_invoice.total_amount,
        "date": db_invoice.date,
        "unit_prices": db_invoice.unit_prices,
        "rent": db_invoice.rent,
        "invoice": result["invoice"]
    }


@router.get("/invoice-preview/{invoice_id}", response_class=PlainTextResponse)
def invoice_preview(invoice_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    try:
        unit_prices_input = invoice.unit_prices.split("+")
        items = []
        quantities = []
        for entry in unit_prices_input:
            if "*" in entry:
                qty, price = entry.split("*")
                qty = int(qty.strip())
                price = float(price.strip())
                items.extend([price] * qty)
                quantities.append((qty, price))
            else:
                price = float(entry.strip())
                items.append(price)
                quantities.append((1, price))
        quantities.sort(key=lambda x: x[1], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse unit_prices: {str(e)}")

    invoice_text = util.calculate_invoice(items, quantities, invoice)["invoice"]
    return invoice_text


@router.post("/invoice-print/{invoice_id}")
def invoice_print(invoice_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # Parse the unit_prices again
    try:
        unit_prices_input = invoice.unit_prices.split("+")
        items, quantities = [], []
        for entry in unit_prices_input:
            if "*" in entry:
                qty, price = entry.split("*")
                items.extend([float(price.strip())] * int(qty.strip()))
                quantities.append((int(qty.strip()), float(price.strip())))
            else:
                price = float(entry.strip())
                items.append(price)
                quantities.append((1, price))
        quantities.sort(key=lambda x: x[1], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error parsing invoice: {str(e)}")

    invoice_text = util.calculate_invoice(items, quantities, invoice)["invoice"]

    try:
        system_os = platform.system()
        if system_os == "Windows":
            # Write to a temp file and print using Notepad
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as temp:
                temp.write(invoice_text)
                temp_path = temp.name
            subprocess.run(["notepad", "/p", temp_path], check=True)
        elif system_os == "Darwin" or system_os == "Linux":
            # Send directly to the default printer
            subprocess.run(["lp"], input=invoice_text.encode(), check=True)
        else:
            raise Exception("Unsupported OS for printing.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Printing failed: {str(e)}")

    return {"message": "Invoice sent to printer successfully"}


@router.get("/invoices", response_model=List[schemas.InvoiceOut])
def get_invoices(db: Session = Depends(get_db)):
    invoices = db.query(models.Invoice).all()
    return invoices
