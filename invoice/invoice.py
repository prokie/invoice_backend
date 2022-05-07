import argparse
import datetime
import os
from math import floor
from pathlib import Path
from shutil import copyfile


class PDFCompany:
    def __init__(self, name, address, city, state, zip_code, phone, manager):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.manager = manager


class PDFWork:
    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate

    def total(self):
        return self.hours * self.rate


class PDFItem:
    def __init__(self, name, price, quantity, unit):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.total = price * quantity
        self.unit = unit

    def get_price(self):
        return "{:,.2f}".format(float("%.2f" % self.price)).replace(",", " ")

    def get_total(self):
        return "{:,.2f}".format(float("%.2f" % self.total)).replace(",", " ")


class PDFInvoiceCustomer:
    def __init__(
        self, name, address, phone, email, city, zip_code, social_security, house
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.city = city
        self.zip_code = zip_code
        self.social_security = social_security
        self.house = house

    def get_zip_code(self):
        return self.zip_code(5)


class PDFInvoice:
    def __init__(
        self,
        customer,
        items,
        company,
        work,
        number,
        my_date,
        due_days,
        start_date,
        end_date,
        rot,
    ):
        self.items = items
        self.number = number
        self.customer = customer
        self.company = company
        self.my_date = datetime.date.fromisoformat(my_date)
        self.due_days = due_days
        self.due_date = self.my_date + datetime.timedelta(days=self.due_days)
        self.work = work
        self.start_date = datetime.date.fromisoformat(start_date)
        self.end_date = datetime.date.fromisoformat(end_date)
        self.rot = rot

    def get_work_date(self):
        if self.start_date == self.end_date:
            return self.start_date.strftime("%Y-%m-%d")
        return (
            self.start_date.strftime("%Y-%m-%d")
            + " - "
            + self.end_date.strftime("%Y-%m-%d")
        )

    def calculate_items_total(self):
        total = 0
        for item in self.items:
            total += item.total
        return "%.2f" % total

    def return_items_total(self):
        return "{:,.2f}".format(float(self.calculate_items_total())).replace(",", " ")

    def get_work_cost(self):
        return "%.2f" % (float(self.work.hours) * float(self.work.rate))

    def return_rot(self):
        return "{:,.2f}".format(
            float("%.2f" % (float(self.work.hours) * float(self.work.rate) * 0.375))
        ).replace(",", " ")

    def calculate_rot(self):
        return "%.2f" % (float(self.work.hours) * float(self.work.rate) * 0.375)

    def calculate_tax(self):
        return "%.2f" % (0.25 * float(self.calculate_items_total()))

    def return_tax(self):
        return "{:,.2f}".format(float(self.calculate_tax())).replace(",", " ")

    def calculate_total_cost_before_rot(self):
        return "%.2f" % (
            float(self.calculate_items_total()) + float(self.calculate_tax())
        )

    def return_total_cost_before_rot(self):
        return "{:,.2f}".format(
            float(
                "%.2f"
                % (float(self.calculate_items_total()) + float(self.calculate_tax()))
            )
        ).replace(",", " ")

    def return_total(self):
        if self.rot:
            return "{:,.2f}".format(
                floor(
                    float(
                        "%.2f"
                        % (
                            float(self.calculate_items_total())
                            + float(self.calculate_tax())
                            - float(self.calculate_rot())
                        )
                    )
                )
            ).replace(",", " ")
        else:
            return "{:,.2f}".format(
                floor(
                    float(
                        "%.2f"
                        % (
                            float(self.calculate_items_total())
                            + float(self.calculate_tax())
                        )
                    )
                )
            ).replace(",", " ")

    def get_social_security(self):
        if len(str(self.customer.social_security)) == 10:
            return (
                str(self.customer.social_security)[0:6]
                + "-"
                + str(self.customer.social_security)[6:]
            )
        return (
            str(self.customer.social_security)[0:8]
            + "-"
            + str(self.customer.social_security)[8:]
        )


class PDFInvoiceCreator:
    def __init__(self, invoice: PDFInvoice, path: Path):
        self.path = path
        self.invoice = invoice

    def get_company_name(self):
        return self.invoice.company.name

    def get_invoice_number(self):
        return self.invoice.number

    def get_items(self):
        my_string = ""
        self.invoice.items.append(
            PDFItem(
                self.invoice.work.name,
                self.invoice.work.rate,
                self.invoice.work.hours,
                "h",
            )
        )
        for index, item in enumerate(self.invoice.items, 1):
            my_string += f"{index} &{item.name} & {item.get_price()} kr & {item.quantity} {item.unit}   & {item.get_total()} kr\\\\\n"

        return my_string

    def create_tex(self):
        with open(self.path / "invoice_test.tex", "w", encoding="utf-8") as f:
            f.write(
                "\\documentclass[PDF11pt]{article}\n"
                "\\setlength{\\headheight}{14pt}\n"
                "\\usepackage[left=0.75in,right=0.75in,bottom=0.75in,top=0.25in]{geometry}\n"
                "\\usepackage[utf8]{inputenc}\n"
                "\\usepackage[swedish]{babel}\n"
                "\\usepackage{tabularx}\n"
                "\\usepackage{microtype}\n"
                "\\usepackage{lastpage}\n"
                "\\usepackage{tcolorbox}\n"
                "\\tcbuselibrary{raster, skins}\n"
                "\\usepackage{fancyhdr}\n"
                "\\pagestyle{fancy}\n"
                "\\usepackage{booktabs} % for table toprule and bottomrule\n"
                "\\newcolumntype{L}[1]{>{\\hsize=#1\\hsize\\raggedright\\arraybackslash}X}\n"
                "\\newcolumntype{R}[1]{>{\\hsize=#1\\hsize\\raggedleft\\arraybackslash}X}\n"
                "\\newcolumntype{C}[1]{>{\\hsize=#1\\hsize\\centering\\arraybackslash}X}\n"
                "\\cfoot{}\n"
                "\\rfoot{\\thepage{} av \\pageref{LastPage}}\n"
                "\\begin{document}\n"
                "\\begin{tcbraster}[raster columns=2, top=0em, noparskip, raster valign=top, raster force size=false]\n"
                "\\begin{tcolorbox}[blankest, fontupper=\\huge, top=0pt,valign=center, height=3.1cm,left=0.2cm]\n"
                f"\\huge{{{self.get_company_name()}}}\n"
                "\\end{tcolorbox}\n"
                "\\begin{tcboxeditemize}[raster columns=2, raster equal height]{blankest}\n"
                "\\tcbitem[raster multicolumn=2, colback=white, top=5pt,valign=center,left=0pt,halign=center] \\huge{Faktura}\n"
                f"\\tcbitem[colback=white] \\textbf{{Fakturanummer}} \\\\ {self.get_invoice_number()+1000}\n"
                f"\\tcbitem[colback=white] \\textbf{{Fakturadatum}} \\\\ {self.invoice.my_date}\n"
                "\\end{tcboxeditemize}\n"
                "\\end{tcbraster}\n"
                "\\begin{tcbraster}[raster columns=2, top=0em, noparskip, raster valign=top, raster force size=false]\n"
                "\\begin{tcolorbox}[blankest]\n"
                "\\textbf{Fakturaadress:} \\\\\n"
                f"{self.invoice.customer.name} \\\\\n"
                f"{self.invoice.customer.address} \\\\\n"
                f"{self.invoice.customer.zip_code} {self.invoice.customer.city}\n"
                "\\end{tcolorbox}\n"
                "\\begin{tcolorbox}[blankest]\n"
                f"\\textbf{{Er referens:}}  {self.invoice.customer.name} \\\\\n"
                f"\\textbf{{Vår referens:}} {self.invoice.company.manager}   \\\\\n"
                f"\\textbf{{Betalningsvilkor:}} {self.invoice.due_days} dagar            \\\\\n"
                f"\\textbf{{Förfallodag:}} {self.invoice.due_date}   \n"
                "\\end{tcolorbox}\n"
                "\\end{tcbraster}\n"
                "\\vspace{0.5cm}\n"
                "\\renewcommand{\\arraystretch}{1.25}\n"
                "\\noindent\n"
                "\\begin{tabularx}{\\textwidth}{  C{0.3}  L{2.9}  C{0.7}  C{0.35} C{0.75}  }\n"
                "\\toprule\n"
                "\\textbf{Post} & \\textbf{Benämning}         & \\textbf{\\`A-pris} & \\textbf{Antal} & \\textbf{Summa} \\\\ \\midrule\n"
                "\\end{tabularx}\n"
                "\\begin{tabularx}{\\textwidth}{  C{0.3}  L{2.9}  R{0.7}  C{0.35} R{0.75}  }\n"
                f"{self.get_items()}\n"
                "\\end{tabularx}\n"
                "\\vfill\n"
                "\\noindent\n"
                "\\begin{tabularx}{\\textwidth}{  L{1.5}  R{1} R{0.5}  }\n"
                f" & Fakturans totala belopp & {self.invoice.return_total_cost_before_rot()} kr \\\\ \n"
                f" & Avgår skattereduktion   & {self.invoice.return_rot()} kr\n"
                "\\end{tabularx}\n"
                "\\noindent\n"
                "\\begin{tabularx}{\\textwidth}{  L{0.5}  L{0.25}  L{0.5} R{1.75}  }\n"
                "\\midrule\n"
                "\\textbf{Exkl. moms} & \\textbf{Moms} & \\textbf{Moms kr} & \\textbf{Att betala} \\\\\n"
                f"{self.invoice.return_items_total()} kr          & 25\\%          & {self.invoice.return_tax()} kr       & {self.invoice.return_total()} kr          \\\\\n"
                "\\bottomrule\n"
                "\end{tabularx}\n"
                "\\vspace{0.2cm}\n"
                "\\begin{tcolorbox}[colback=white]\n"
                f"Denna faktura avser ROT-arbete på fastigheten {self.invoice.customer.house}. Köparens personnummer {self.invoice.get_social_security()}.\n"
                f"Enligt dig som köpare finns det möjlighet till preliminär skattereduktion på {self.invoice.return_rot()} kr, 30\\% av arbetskostnaden inkl. moms.\n"
                f"Arbetet är utfört {self.invoice.get_work_date()}.\n"
                "\\end{tcolorbox}\n"
                "\\vspace{0.5cm}\n"
                "\\begin{tcbraster}[raster columns=4, top=0em, noparskip, raster valign=top, raster force size=false]\n"
                "\\begin{tcolorbox}[blankest]\n"
                "\\textbf{Adress} \\\\\n"
                "Magnus Thomsson \\\\\n"
                "Tallundsgatan 8  \\\\\n"
                "621 58~~Visby     \n"
                "\\end{tcolorbox}\n"
                "\\begin{tcolorbox}[blankest]\n"
                "\\textbf{Betalningsuppgifter} \\\\\n"
                "Bankgiro: 5498-7219  \\\\ \n"
                "Bank: Swedbank\n"
                "\\end{tcolorbox}\n"
                "\\begin{tcolorbox}[blankest]\n"
                "\\textbf{Kontakt} \\\\\n"
                "0739 73 61 24\n"
                "\\end{tcolorbox}\n"
                "\\begin{tcolorbox}[blankest]\n"
                "\\textbf{Momsreg.nr} \\\\ \n"
                "SE660928321001 \\\\ \n"
                "Godkänd för F-skatt\n"
                "\\end{tcolorbox}\n"
                "\\end{tcbraster}\n"
                "\\end{document}\n"
            )

    def run_latexmk(self, name):
        os.system(
            f'latexmk -output-directory="{self.path}\output" -pdf {self.path}\invoice_test.tex -silent'
        )
        copyfile(
            Path(f"{self.path}/output/invoice_test.pdf"),
            Path(f"D:/Projects/Invoice/{name}.pdf"),
        )


def main(args=None):
    my_item = PDFItem("Test", 100.60, 1)
    my_item1 = PDFItem("Test1", 100.60, 5)
    my_company = PDFCompany(
        "company name",
        "company address",
        "company city",
        "Company state",
        "company postkod",
        "company phone",
        "Magnus Thomsson",
    )
    my_customer = PDFInvoiceCustomer(
        "Albin Thomsson",
        "Luleåvägen 123",
        "0700598666",
        "albin_lit@gmail.com",
        "Luleå",
        "12345",
    )
    my_work = PDFWork("Arbetstid", 3, 450)
    my_invoice = PDFInvoice(my_customer, [my_item, my_item1], my_company, my_work)
    invoice = PDFInvoiceCreator(my_invoice, args.path)
    invoice.create_tex()
    invoice.run_latexmk()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Invoice")
    parser.add_argument("-n", "--number", help="Invoice Number", default="1")
    parser.add_argument(
        "-i", "--items", help="Items", nargs="+", default=["Item 1", "Item 2"]
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Path to Invoice",
        default="D:/Projects/Invoice/latex",
        type=Path,
    )
    args = parser.parse_args()
    main(args)
