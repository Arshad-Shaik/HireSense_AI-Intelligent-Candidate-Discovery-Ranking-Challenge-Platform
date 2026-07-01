# ai-service/filters/company_classifier.py

def classify_company(
        company_name
):
    """
    Classify company type.

    Returns:
        product
        service
        unknown
    """

    if not company_name:
        return "unknown"

    company = company_name.lower()

    service_companies = {

        "tcs",
        "infosys",
        "wipro",
        "accenture",
        "capgemini",
        "cognizant",
        "hcl",
        "tech mahindra",
        "ibm gbs"
    }

    if company in service_companies:

        return "service"

    return "product"