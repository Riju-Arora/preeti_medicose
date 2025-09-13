from decimal import Decimal
import pandas as pd
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = "Import products from Excel"

    def add_arguments(self, parser):
        parser.add_argument("excel_file", type=str)

    def handle(self, *args, **kwargs):
        excel_file = kwargs["excel_file"]
        df = pd.read_excel(excel_file)

        # Clean headers
        df.columns = df.columns.str.strip().str.lower()

        for _, row in df.iterrows():
            try:
                mrp = Decimal(str(row["mrp"])) if row["mrp"] not in [None, ""] else Decimal("0.00")
                price = Decimal(str(row["price"])) if row["price"] not in [None, ""] else Decimal("0.00")


                # Auto discount calculation (if mrp > price)
                discount_percent = 0
                if mrp > 0 and price > 0 and mrp > price:
                    discount_percent = round(((mrp - price) / mrp) * 100, 2)

                product, created = Product.objects.get_or_create(
                    name=row["name"],
                    defaults={
                        "description": str(row.get("description", "")),
                        "mrp": mrp,
                        "price": price,
                        "category": row.get("category", "other"),
                    }
                )

                if not created:
                    # update existing product
                    product.description = str(row.get("description", ""))
                    product.mrp = mrp
                    product.price = price
                    product.category = row.get("category", "other")
                    product.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ {product.name} imported (MRP: {mrp}, Price: {price}, Discount: {discount_percent}%)"
                    )
                )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error on {row['name']}: {e}"))
