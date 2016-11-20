"""
# The precision score is defined as follows:
Precision = Total number of correctly predicted entities/ Total number of predicted entities

# The recall score is defined as follows:
Recall = Total number of correctly predicted entities/ Total number of gold entities

where a gold entity is a true entity that is annotated in the reference output file, and a predicted entity
is regarded as correct if and only if it matches exactly the gold entity (i.e., both their boundaries and
sentiment are exactly the same).

# Finally the F score is defined as follows:
F = 2/ (1/Precision + 1/Recall)
"""