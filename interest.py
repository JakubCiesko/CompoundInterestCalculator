from input_handling import Input, InputGroup

def get_quotient(p_a:float) -> float: 
    """
    Calculates the quotient for interest rate adjustment.

    Args:
        p_a (float): The interest rate per annum (percentage).

    Returns:
        float: The quotient for interest calculation, 1 + p_a / 100.
    """
    return (1 + p_a/100)

def interest(base:float, p_a:float) -> float: 
    """
    Calculates the interest based on the base amount and interest rate.

    Args:
        base (float): The principal or base amount.
        p_a (float): The annual interest rate (percentage).

    Returns:
        float: The total amount after applying interest.
    """
    return base * get_quotient(p_a)

def compound_interest(base:float, p_a:float, years:int, monthly:float=0.0, **kwargs) -> float:
    """
    Calculates the compound interest over a given number of years with optional monthly contributions.

    Args:
        base (float): The initial base amount.
        p_a (float): The annual interest rate (percentage).
        years (int): The number of years the interest is applied.
        monthly (float, optional): Monthly contribution amount. Defaults to 0.0.
        **kwargs: Additional arguments (not used).

    Returns:
        float: The total final amount after compounding interest and monthly contributions.
    """ 
    final = base 
    for _ in range(years):
        final += 12*monthly
        final = interest(final, p_a)
    return final 

def base_amount(final:float, p_a:float, years:int, monthly:float=0.0, **kwargs) -> float:
    """
    Calculates the base amount needed to reach a given final amount after interest and contributions.

    Args:
        final (float): The final amount to reach.
        p_a (float): The annual interest rate (percentage).
        years (int): The number of years the interest is applied.
        monthly (float, optional): Monthly contribution amount. Defaults to 0.0.
        **kwargs: Additional arguments (not used).

    Returns:
        float: The base amount required to reach the final amount.
    """
    base = final 
    quotient = get_quotient(p_a)
    for _ in range(years):
        base /= quotient 
        base -= 12*monthly 
    return base 

def monthly(final:float, base:float, p_a:float, years:int, **kwargs) -> float:
    """
    Calculates the required monthly contribution to reach a final amount from a base amount with compounding interest.

    Args:
        final (float): The final target amount.
        base (float): The initial base amount.
        p_a (float): The annual interest rate (percentage).
        years (int): The number of years the interest is applied.
        **kwargs: Additional arguments (not used).

    Returns:
        float: The monthly contribution needed to reach the final amount.
    """ 
    quotient = get_quotient(p_a)
    numerator = final - base*quotient**years
    denominator = 12*sum(quotient**i for i in range(years))
    return numerator / denominator


if __name__ == "__main__":
    conditions = InputGroup({
        "base": Input(),
        "p_a": Input(),
        "years": Input(),
        "monthly": Input(),
    })
    
    conditions["base"].read("Base amount:\t", float)
    conditions["p_a"].read("Per annum interest rate:\t", float)
    conditions["years"].read("Number of years:\t", int)
    conditions["monthly"].read("Monthly contribution:\t", float)

    arguments = {
        "base": conditions["base"].get(),
        "p_a": conditions["p_a"].get(),
        "years": conditions["years"].get(),
        "monthly": conditions["monthly"].get(),
    }
    
    print("Final saved amount:\t", final:=compound_interest(**arguments))
    #Run for correction check:
    #print(base_amount(final, **arguments))
    #print(monthly(final, **arguments))