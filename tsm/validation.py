

def validate_single_parser(forms):
    if len(forms) == 1:
        form = forms[0]
        if form.is_valid():
            if form.cleaned_data['start_time']:
                form.add_error('start_time', 'Leave empty if just one Parser.')
            if form.cleaned_data['end_time']:
                form.add_error('end_time', 'Leave empty if just one Parser.')
    # if there is one parser there should be no start and end => could be hidden...


def check_parser_time_ranges(forms):
    parsers = []
    for form in forms:
        if form.is_valid():
            parser = form.cleaned_data
            parsers.append(parser)

    for index, parser in enumerate(parsers):
        next_pos = index + 1
        if next_pos >= len(parsers):
            break

        next_parser = parsers[next_pos]
        if parser['end_time'] != next_parser['start_time']:
            forms[0].add_error('end_time', 'Please check that Parser-Endtime always matches the next Parser-Starttime.')


def get_number_of_valid_forms(forms):
    count = 0
    for form in forms:
        if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
            count += 1
    return count


def check_required_fields(forms, fields):
    for form in forms:
        if form.is_valid():
            form_data = form.cleaned_data
            for field in fields:
                if form_data[field]:
                    continue
                form.add_error(field, 'This field could not be empty.')
