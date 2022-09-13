

def validate_fields(forms, fields):
    for form in forms:
        if form.is_valid():
            form_data = form.cleaned_data
            for field in fields:
                if form_data[field]:
                    continue
                form.add_error(field, 'This field could not be empty.')


def get_number_of_valid_forms(forms):
    count = 0
    for form in forms:
        if form.is_valid():
            count += 1
    return count
