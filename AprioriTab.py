import ast
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog

# External modules
from File_Loader import load_transactions
from Apriori_Algo import apriori, generate_association_rules

class AprioriTab:
    def __init__(self, parent):
        frame = tb.Frame(parent, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        tb.Label(frame, text="CSV File:").grid(row=0, column=0, sticky=W)
        self.filepath_var = tb.StringVar(master=frame)
        tb.Entry(frame, textvariable=self.filepath_var, width=60).grid(row=0, column=1, padx=5)
        tb.Button(frame, text="Browse", bootstyle=PRIMARY, command=self.browse_file).grid(row=0, column=2, padx=5)

        self.input_mode = tb.StringVar(value="file")
        tb.Label(frame, text="Input Mode:").grid(row=1, column=0, sticky=W, pady=5)
        tb.Radiobutton(frame, text="Load from File", variable=self.input_mode, value="file").grid(row=1, column=1, sticky=W)
        tb.Radiobutton(frame, text="Enter Transactions", variable=self.input_mode, value="manual").grid(row=1, column=2, sticky=W)

        tb.Label(frame, text="Manual Input:").grid(row=2, column=0, columnspan=3, sticky=W, pady=(10, 0))
        self.manual_input_text = ScrolledText(frame, height=7, width=100, font=("Consolas", 10))
        self.manual_input_text.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        tb.Label(frame, text="Min Support:").grid(row=4, column=0, sticky=W, pady=5)
        self.support_var = tb.DoubleVar(value=0.02)
        tb.Entry(frame, textvariable=self.support_var, width=10).grid(row=4, column=1, sticky=W)

        tb.Label(frame, text="Min Confidence:").grid(row=5, column=0, sticky=W, pady=5)
        self.confidence_var = tb.DoubleVar(value=0.3)
        tb.Entry(frame, textvariable=self.confidence_var, width=10).grid(row=5, column=1, sticky=W)

        tb.Button(frame, text="Run Apriori", bootstyle=SUCCESS, command=self.run_apriori).grid(row=6, column=1, pady=10, sticky=W)

        self.output_text = ScrolledText(frame, wrap='word', width=100, height=18, font=("Consolas", 10))
        self.output_text.grid(row=7, column=0, columnspan=3, pady=10)

    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            self.filepath_var.set(filepath)

    def run_apriori(self):
        try:
            if self.input_mode.get() == "file":
                filepath = self.filepath_var.get()
                transactions = load_transactions(filepath)
            else:
                raw_input = self.manual_input_text.get("1.0", "end").strip().splitlines()
                transactions = [ast.literal_eval(line.strip()) for line in raw_input if line.strip()]

            min_support = self.support_var.get()
            min_confidence = self.confidence_var.get()

            self.output_text.delete("1.0", "end")

            frequent_itemsets, _ = apriori(transactions, min_support)
            self.output_text.insert("end", "\U0001F4E6 Frequent Itemsets:\n")
            for itemset, support in frequent_itemsets.items():
                self.output_text.insert("end", f"{set(itemset)}: {support:.2f}\n")

            rules = generate_association_rules(frequent_itemsets, min_confidence, transactions)
            self.output_text.insert("end", "\n\U0001F517 Association Rules:\n")
            for antecedent, consequent, confidence in rules:
                self.output_text.insert("end", f"{set(antecedent)} => {set(consequent)} (Confidence: {confidence:.2f})\n")

        except Exception as e:
            Messagebox.show_error(f"Error: {e}", title="Error")
