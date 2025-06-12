from fastapi import HTTPException, status
from datetime import datetime
from app import schemas


def create_invoice(invoice: schemas.InvoiceCreate):
    items = []
    quantities = []

    try:
        unit_prices_input = invoice.unit_prices.split("+")
        for entry in unit_prices_input:
            if '*' in entry:
                qty, price = entry.split('*')
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
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Invalid format in unit_prices. Error: {str(e)}"
        )

    return items, quantities


def calculate_invoice(items, quantities, invoice: schemas.InvoiceCreate):
    width = 48
    rent = invoice.rent
    customer_name = invoice.customer_name
    date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    subtotal = sum(items)
    total_quantity = sum(qty for qty, _ in quantities)
    comm = 0.04 * subtotal
    wastage = 0.06 * subtotal
    gate = 5 * sum(qty for qty, price in quantities if price > 200)

    deductions = round(comm + wastage + rent + gate + gate + total_quantity)
    deductions_bill = round(deductions / 10) * 10
    total = subtotal - deductions_bill

    invoice_text = (
        f"{'SRI SHIVA SANKAR LEMON COMPANY':^{width}}\n"
        f"{'MARKET YARD, R.F ROAD, TADIPATRI':^{width}}\n"
        f"{'SEENA - 9440347321 , SRINATH - 9493559204 ':^{width}}\n"
        f"{'-' * width}\n"
        f"Customer: {customer_name}\n"
        f"Date: {date_time}\n"
        f"{'-' * width}\n"
        f"{'Quantity':<14}| {'Unit Price':<14}| {'Total ':<14}\n"
        f"{'-' * width}\n"
    )

    for qty, price in quantities:
        total_price = qty * price
        invoice_text += f"{qty:<14}| {price:<14.2f}| {total_price:<14.2f}\n"

    invoice_text += (
        f"{'-' * width}\n"
        f"{total_quantity:<14}| {'Subtotal':<14}| {subtotal:<14.2f}\n"
        f"{'':<14}| {'Deductions(-)':<14}| {deductions_bill:<14.2f}\n"
        f"{'-' * width}\n"
        f"{'':<7}| {'Total':<6}:{total:<6.2f}\n"
        f"{'-' * width}\n"
        f"Deduction calculations:\n"
        f"Comm @ 4%:   {comm:.2f} \n"
        f"Wastages :   {wastage:.2f} \n"
        f"Rent     :   {rent:.2f} \n"
        f"Gate     :   {gate:.2f} \n"
        f"Unloading:   {gate:.2f} \n"
        f"Yard     :   {total_quantity:.2f} \n"
        f"{'-' * 20}\n"
        f"         {deductions:.2f} \n"
        f"{'Thank You & Visit Again':^{width}}\n"
    )

    return {
        "customer_name": customer_name,
        "total_quantity": total_quantity,
        "total_amount": total,
        "date": date_time,
        "rent": rent,
        "invoice": invoice_text
    }
