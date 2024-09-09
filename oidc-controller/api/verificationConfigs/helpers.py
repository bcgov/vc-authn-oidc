from .variableSubstitutions import variable_substitution_map


def replace_proof_variables(proof_req_dict: dict) -> dict:
    """
    Recursively replaces variables in the proof request with actual values.
    The map is provided by imported variable_substitution_map.
    Additional variables can be added to the map in the variableSubstitutions.py file,
    or other dynamic functionality.

    Args:
        proof_req_dict (dict): The proof request dictionary from the resolved config.

    Returns:
        dict: The updated proof request dictionary with placeholder variables replaced.
    """

    for k, v in proof_req_dict.items():
        # If the value is a dictionary, recurse
        if isinstance(v, dict):
            replace_proof_variables(v)
        # If the value is a list, iterate trhough list items and recurse
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    replace_proof_variables(i)
        # If the value is a string and matches a key in the map, replace it
        elif isinstance(v, str):
            if v in variable_substitution_map:
                proof_req_dict[k] = variable_substitution_map[v]()
        # Base case: If the value is not a dict, list, or matching string, do nothing
    return proof_req_dict
