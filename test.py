fields_name = ["timestamps", "program_name", "product_SKU", "request_type",
               "request_url", "client_ip", "query", "request_service", "resource_type",
               "resource_id", "description", "result_count", "response_code",
               "response_time", "user_id", "user_account", "group_account",
               "library_card", "referer_url", "thread_id", "session_id", "search_id",
               "request_id", "content_length", "session_sequence", "grade",
               "user_role", "server", "hostname", "owner_id", "search_mode",
               "delivery_method", "access_method", "selling_method", "contract_type",
               "delivery_format", "document_source", "dumy1", "content_type",
               "authentication_method", "language", "interface_type", "dumy2",
               "subscription_id", "usage_type", "user_agent"]

file_size = 0
fields_dict = dict()

def load_sections(filename):
  region_file = open(filename, 'rU')
  index = 0
  #create a list for each field
  for x in fields_name:
    fields_dict[fields_name[index]] = []
    index += 1
  index = 0
  
  is_firstline = True
  for line in region_file:
    if is_firstline:
      is_firstline = False
      continue

    fields = line.split(";;|")

    #add each line of log files into each fields list
    for field in fields:
      fields_dict[fields_name[index]].append(field) # field
      index += 1

    index = 0
  region_file.close()
  return


def print_dict_list_mode(my_dict):
  for field in fields_name:
    print field, ": " ,my_dict[field]
  return


def main():
  load_sections("log1.txt")
  #print_dict(fields_dict)

  print_dict_list_mode(fields_dict)


main();

#test