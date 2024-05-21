class Taxpayer:
    def __init__(self, name, gross_income, num_children, education_allowance, self_education_allowance, donations, nppf_contribution, gis_contribution):
        # Initialize the taxpayer's attributes with provided values.
        self.name = name
        self.gross_income = gross_income
        self.num_children = num_children
        # Cap education allowance per child to 350,000.
        self.education_allowance = min(350000 * num_children, education_allowance)
        # Cap self-education allowance to 350,000.
        self.self_education_allowance = min(350000, self_education_allowance)
        # Cap donations to 5% of gross income.
        self.donations = min(0.05 * gross_income, donations)
        self.nppf_contribution = nppf_contribution
        self.gis_contribution = gis_contribution

    def calculate_taxable_income(self):
        # Calculate total deductions.
        total_deductions = (
            self.education_allowance +
            self.self_education_allowance +
            self.donations +
            self.nppf_contribution +
            self.gis_contribution
        )
        # Calculate taxable income by subtracting deductions from gross income.
        taxable_income = self.gross_income - total_deductions
        # Ensure taxable income is not negative.
        return max(taxable_income, 0)

    def calculate_tax(self):
        # Get the taxable income.
        taxable_income = self.calculate_taxable_income()
        # Determine tax based on taxable income brackets.
        if taxable_income <= 300000:
            return 0
        elif taxable_income <= 400000:
            return (taxable_income - 300000) * 0.10
        elif taxable_income <= 650000:
            return 10000 + (taxable_income - 400000) * 0.15
        elif taxable_income <= 1000000:
            return 47500 + (taxable_income - 650000) * 0.20
        elif taxable_income <= 1500000:
            return 117500 + (taxable_income - 1000000) * 0.25
        else:
            base_tax = 242500 + (taxable_income - 1500000) * 0.30
            # Add a 10% surcharge if taxable income exceeds 1,000,000.
            if taxable_income > 1000000:
                base_tax += 0.10 * base_tax  # 10% surcharge
            return base_tax


class RegularEmployee(Taxpayer):
    def __init__(self, name, gross_income, num_children, education_allowance, self_education_allowance, donations, nppf_contribution, gis_contribution):
        # Initialize a regular employee, which includes NPPF contribution.
        super().__init__(name, gross_income, num_children, education_allowance, self_education_allowance, donations, nppf_contribution, gis_contribution)


class ContractEmployee(Taxpayer):
    def __init__(self, name, gross_income, num_children, education_allowance, self_education_allowance, donations, gis_contribution):
        # Initialize a contract employee, who does not contribute to NPPF.
        super().__init__(name, gross_income, num_children, education_allowance, self_education_allowance, donations, 0, gis_contribution)


def main():
    try:
        # Gather input from the user.
        name = input("Enter the name of the taxpayer: ")
        gross_income = float(input("Enter the gross income: "))
        num_children = int(input("Enter the number of children: "))
        education_allowance = float(input("Enter the education allowance: "))
        self_education_allowance = float(input("Enter the self education allowance: "))
        donations = float(input("Enter the amount of donations: "))
        nppf_contribution = float(input("Enter the NPPF contribution: "))
        gis_contribution = float(input("Enter the GIS contribution: "))
        is_contract_employee = input("Is the individual a contract employee? (yes/no): ").strip().lower() == 'yes'

        # Create an employee object based on whether they are a contract employee.
        if is_contract_employee:
            employee = ContractEmployee(name, gross_income, num_children, education_allowance, self_education_allowance, donations, gis_contribution)
        else:
            employee = RegularEmployee(name, gross_income, num_children, education_allowance, self_education_allowance, donations, nppf_contribution, gis_contribution)

        # Calculate the tax payable and print the result.
        tax_payable = employee.calculate_tax()
        print(f"{employee.name} has to pay Nu. {tax_payable:.2f} in tax.")

    except ValueError:
        # Handle invalid input errors.
        print("Invalid input. Please enter numeric values for income, allowances, and contributions.")

if __name__ == "__main__":
    main()
