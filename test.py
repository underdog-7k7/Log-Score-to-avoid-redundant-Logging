from google.colab import files
file = files.upload()



# import re

# def extract_class_data(java_code):
#     data_members = {}
#     member_functions = {}
#     classes = []

#     # Regex patterns
#     data_member_pattern = r"(?:(?:private|public|protected|static|final|abstract)\s+)+([\w<>?,\[\]\s]+)\s+(\w+);"
#     member_function_pattern = r"(?:(?:private|public|protected|static|final|abstract)\s+)*([\w<>?,\[\]\s]+)\s+(\w+)\s*\(([^)]*)\)\s*\{"

#     # Extract data members
#     matches = re.findall(data_member_pattern, java_code)
#     for match in matches:
#         data_type, data_member = match
#         data_members[data_member] = data_type.strip()

#     # Extract member functions
#     matches = re.findall(member_function_pattern, java_code)
#     for match in matches:
#         return_type, member_function, parameters = match
#         parameter_list = [param.strip() for param in parameters.split(",")]
#         member_functions[member_function] = [return_type.strip(), parameter_list]

#     # Extract classes
#     class_pattern = r"(?:(?:private|public|protected|static|final|abstract)\s+)?(?:class|interface)\s+(\w+)\s*\{"
#     matches = re.findall(class_pattern, java_code)
#     classes = matches

#     # Prepare and return the dictionary
#     result = {
#         "data_members": data_members,
#         "member_functions": member_functions,
#         "classes": classes
#     }
#     return result

# java_code = content

# class_name = "Main"
# class_data = extract_class_data(java_code, class_name)
# print(class_data)


import os

file_name = "Main.java"
with open(file_name, "r") as file:
  content = file.read()
  # saving acopy of original code
  original = content

original = '''
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.lang.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
public class Main {

    private static final Logger LOGGER = Logger.getLogger(Main.class.getName());
    private static int max = 50;


    public static void logTimeComplexity(String functionName, String timeComplexity) {
        LOGGER.log(Level.INFO, functionName + " has a time complexity of " + timeComplexity);
    }


    public static void function1(int[] arr) {
        // O(n)
        int sum = 0;
        for (int num : arr) {
            sum += num;
            logTimeComplexity("function1", "O(n)");
        }
    }

    public static void function2(int[] arr) {
        // O(n^2)
        int product = 1;
        for(int k=0;k<24;k++){
          product = product*k;
        }
        for (int i = 0; i < arr.length; i++) {
            for (int j = i + 1; j < arr.length; j++) {
              for(int l=0;l<arr.length;l++){
                product *= arr[i] * arr[j];
                  LOGGER.log(Level.INFO, product);
              }
            }
        }
        logTimeComplexity("function2", "O(n^2)");
    }

    public static void function3(int[] arr) {
        // O(nlog n)
        Arrays.sort(arr);
        if(arr.length()==0){
          return;
        }
        int[] cpy = Arrays.copyOf(arr,arr.length()-1);
        function3(cpy);
//        int target = 5;
//        int low = 0;
//        int high = arr.length - 1;
//        while (low <= high) {
//            int mid = (low + high) / 2;
//            if (arr[mid] == target) {
//                break;
//            } else if (arr[mid] < target) {
//                low = mid + 1;
//            } else {
//                high = mid - 1;
//            }
//        }
        logTimeComplexity("function3", "recursion");
    }
    public static int[] readIntArrayFromFile(String fileName) {
        try{
          BufferedReader reader = new BufferedReader(new FileReader(fileName)) {
          String line = reader.readLine();
          if (line != null) {
              line = line.trim();
              if (line.startsWith("{") && line.endsWith("}")) {
                  line = line.substring(1, line.length() - 1).trim();
                  String[] parts = line.split(",");
                  int[] array = new int[parts.length];
                  for (int i = 0; i < parts.length; i++) {
                      array[i] = Integer.parseInt(parts[i].trim());
                      logTimeComplexity("function3", "O(nlog n)");
                  }
                  return array;
              }
          }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
    public static void main(String[] args) {
        int[] arr = readIntArrayFromFile("src/array.txt");
        long startTime;
        long endTime;
        long executionTime;
        logTimeComplexity("Demo","trial");
        startTime = System.currentTimeMillis();
        function1(arr);
        endTime = System.currentTimeMillis();
        executionTime = endTime - startTime;
        System.out.println("Execution time function1: " + executionTime + "ms");
        startTime = System.currentTimeMillis();
        function2(arr);
        endTime = System.currentTimeMillis();
        executionTime = endTime - startTime;
        System.out.println("Execution time function2: " + executionTime + "ms");
        startTime = System.currentTimeMillis();
        function3(arr);
        endTime = System.currentTimeMillis();
        executionTime = endTime - startTime;
        System.out.println("Execution time function3: " + executionTime + "ms");
    }
}
'''
content = original

# Handling Comments and Multi-line Comments

import re
# print(content)
comment_pattern = r"(?://[^\n]*|/\*(?:.|[\r\n])*?\*/|/\*\*(?:.|[\r\n])*?\*/)"
comments = re.findall(comment_pattern, content)
# print(comments)
for comment in comments:
    content = content.replace(comment,"")
print(content)



import re

def evaluate_operation(operation, variable_dict):
  for var, value in variable_dict.items():
    operation = re.sub(r'\b' + re.escape(var) + r'\b', str(value), operation)
    # print(operation)
  try:
    return eval(operation)
  except:
    return operation

def parse_java_code(java_code):
  variable_dict = {}
  cont_dict = {}
  assignment_regex = r'(\w+)\s*=\s*([^<>]*)\s*;'
  array_regex = r'(\w+[\[\]]+)\s*=\s*([^<>=]*)\s*;'
  b_array_regex = r'\s*.*(\[\]\s*\w|\w+\[\]).*=(\s*.*);'
  unary_operator_handler = r'((\w)\s*([+\-*/%]))\s*=(.*)'
  clone_regex = r'=(.*\.(copy.*|clone.*)\((.*)\)).*'
  col_regex = r'\<.*\>\s*(\w+)=\s*(.*);'
  itr_regex = r'(\w+)\s*=\s*(\w+)\..*iterator.*'
  lines = java_code.split("\n")

  for line in lines:
    line = line.replace("++","+=1")
    line = line.replace("--","+=1")
    unary_matches = re.findall(unary_operator_handler, line,re.IGNORECASE|re.MULTILINE)
    if len(unary_matches):
      for found_match in unary_matches:
        # print(found_match)
        to_replace, var, operator, value = found_match
        line = re.sub(r'\b' + re.escape(to_replace), var, line)
        line = re.sub(r'\b' + re.escape(value)  , var+operator+value, line)
    # print(line)


    col_matches = re.findall(col_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(col_matches):
      for cmatch in col_matches:
        # print(cmatch)
        variable, size = cmatch
        numbers = re.findall(r'\((\d+)\)',size)
        # print(numbers)
        if len(numbers):
          size = int(numbers[0])
          cont_dict[variable] = size
          variable_dict[variable+'.size()'] = size
        else:
          cont_dict[variable] = size

    clone_matches = re.findall(clone_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(clone_matches):
      for cmatch in clone_matches:
        # print(cmatch)
        to_replace, func, value = cmatch
        numbers = re.findall(r'\d+',value)
        # print(numbers)
        if len(numbers):
          size = numbers[0]
          for i in range(1,len(numbers)):
            size = abs(numbers[i]-size)
          # print(size)
          line = re.sub(r'' + re.escape(to_replace), size, line)
          # print(line)
        else:
          line = re.sub(r'' + re.escape(to_replace), value, line)


    array_matches = re.findall(b_array_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(array_matches):
      for amatch in array_matches:
        # print(amatch)
        variable, size = amatch
        numbers = re.findall(r'\[(\d+)\]',size)
        # print(numbers)
        if len(numbers):
          size = int(numbers[0])
          for i in range(1,len(numbers)):
            size = abs(int(numbers[i])*size)
          # print(size)
          variable = variable.replace("[","")
          variable = variable.replace("]","")
          cont_dict[variable] = size
          variable_dict[variable+'.length'] = size
        else:
          variable = variable.replace("[","")
          variable = variable.replace("]","")
          cont_dict[variable] = size
          variable_dict[variable+'.length'] = size


    assignment_match = re.findall(assignment_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(assignment_match):
      variable_name, variable_value = assignment_match[0]
      # print(f"variable_name:{variable_name} variable_value:{variable_value}")

      evaluated_value = evaluate_operation(variable_value, variable_dict)
      if evaluated_value is not None:
        variable_dict[variable_name] = evaluated_value
      else:
        variable_dict[variable_name] = variable_value


    itr_matches = re.findall(itr_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(itr_matches):
      for imatch in itr_matches:
        print(imatch)
        variable, size = imatch
        try:
          size=cont_dict[size]
        except:
          try:
            size=variable_dict[size+".size()"]
          except:
            size =size

        variable_dict[variable] = size

    for var in variable_dict.keys():
      try:
        variable_dict[var] = evaluate_operation(variable_dict[var], variable_dict)
        variable_dict[var] = cont_dict[variable_dict[var]]
        variable_dict[var] = evaluate_operation(variable_dict[var], cont_dict)
      except:
        continue

  return variable_dict, cont_dict

# Example Java code
java_code = '''
int x = n;
String s = "Abu";
int[][] a = new int[5][10];
int c[] = new int[10];
int b[] = Arrays.copyOf(a);
HashMap<Integer, Integer> map= new HashMap<>(10);
x++;
int y = 10;
y++;
int z = x + y;
x = x * 2;
int n = 2;
for(int i=x; i<n;i++){
  //loop
}
Iterator<Integer> m = map.iterator();
ListIterator<String> crunchifyListIterator = crunchifyList.listIterator();
'''

parsed_variables, parsed_containers = parse_java_code(java_code)
print(parsed_variables)
print(parsed_containers)


# Demonstration of new Entry Point to extract log information based on line number

import re
def chk_if_closed(cur,end,split_content):
  chk=[]
  i = cur+1
  while i<end:
    if "{" in split_content[i]:
     chk.append("{")
    if "}" in split_content[i] and len(chk)==0:
      return True
    if "}" in split_content[i] and chk[-1]=="{":
      chk.pop()

    i+=1
  return False

def extract_log_func(p,content,space_score,ignore):
  split_content = content.split("\n")
  complex_score = 1;
  log_func_info = {}
  parent_func_info = {}
  space_score = 1;
  for no, code in enumerate(split_content):
    log_func_matches = re.findall(r'\b'+re.escape(p)+'\s*\(', code, re.MULTILINE|re.IGNORECASE)
    if len(log_func_matches) and no!=ignore:
      for lmatch in log_func_matches:
        log_func_info[no] = get_log_state(split_content, no)
        parent = log_func_info[no]["parent_func"]
        ignore = log_func_info[no]["parent_line"]
        for par in parent:
          if p==par:
            try:
              print(f"function {p} appears to be called recursively.Enter size of function arguments:")
              print(split_content[no])
              args = log_func_info[no]["parent_args"].split(",")
              if len(args)>1:
                max_a = 1
                for a in args:
                  val = int(input(f"Enter size/value for: {a}"))
                  if(val>max_a):
                    max_a = val
                complex_score = complex_score*(2**max_a)*log_func_info[no]["complex_score"]
              else:
                args = log_func_info[no]["parent_args"]
                val = int(input(f"Enter size/value for: {args}"))
                complex_score = (2**val) *log_func_info[no]["complex_score"]
              except:
              args = log_func_info[no]["parent_args"]
              val = int(input(f"Enter size/value for: {args}"))
              complex_score = (2**val) *log_func_info[no]["complex_score"]
            space_score = space_score+(space_score*log_func_info[no]["complex_score"])
          else:
            # print(space_score)
            # print(log_func_info[no]["complex_score"])
            space_score = space_score+(space_score*log_func_info[no]["complex_score"])
            complex_score = complex_score*log_func_info[no]["complex_score"]
            ignore = log_func_info[no]["parent_line"]
            parent_func_info[no] = extract_log_func(par,content,space_score,ignore)
  result={
        "complex_score":complex_score,
        "log_func_info": log_func_info,
        "parent_func_info":parent_func_info,
        "space_score": space_score
    }

  return result



def get_log_state(split_content, line_no):
  parent_func = set()
  parent_args = set()
  score_metric = []
  to_spare = 0
  chk_passed = []
  need_input = []
  debug_help = {}
  entire_content =""
  cur = line_no
  start = 0
  for_while_chk = r'(for|while)\s*\((.+)\)'
  for_each_chk = r'(\w+)\..*(forEach)'
  stop = False
  while(cur>0 and not stop):
    cur = cur-1
    cur_line = split_content[cur]+split_content[cur+1]
    fun_chk = r'\w+\s*(\w+)\s*=*\s*\((.*)\).*{'
    matches = re.findall(fun_chk, cur_line, re.MULTILINE|re.IGNORECASE)
    for fmatch in matches:
      fun, arg = fmatch
      if ";" in arg or ":" in arg or "&&" in arg or "||" in arg:
        continue
      else:
        if len(arg.split(" ")) == 1 and len(arg)!=0:
          continue
        else:
          parent_func.add(fun)
          for a in arg.split(","):
            parent_args.add(a)
          debug_help[fun] = {"line":cur,"->":cur_line}
          start = cur
          stop = True
          break
  print(f"Inside Function:{list(parent_func)}")
  cur = start
  while(cur<line_no):
    if cur==line_no-1 or ("{" in split_content[cur] or "{" in split_content[cur+1]):
      entire_content= entire_content +"\n"+ split_content[cur]
      cur_line = split_content[cur]
      parsed_variables, parsed_containers = parse_java_code(entire_content)
      # print(parsed_variables)
      # print(parsed_containers)
      # print(entire_content)
      fw_matches = re.findall(for_while_chk, cur_line,re.IGNORECASE|re.MULTILINE)
      # print(cur_line)
      if len(fw_matches):
        # print(f"For-while: {fw_matches}")
        chk_passed.append(cur)
        for imatch in fw_matches:
          # print(imatch)
          it, arg = imatch
          debug_help[cur] = {"line":f"{len(score_metric)}","->":cur_line}
          match_fnd = re.findall(r'(\w+)\s*:\s*(\w+)',arg,re.IGNORECASE|re.MULTILINE)
          for fnd in match_fnd:
            toset, var = fnd
            if var:
              try:
                score_metric.append(parsed_variables[var])
                parsed_variables[toset] = parsed_variables[var]
              except:
                try:
                  score_metric.append(parsed_containers[var])
                  parsed_variables[toset] = parsed_containers[var]
                except:
                  try:
                    score_metric.append(parsed_variables[var+".size()"])
                    parsed_variables[toset] = score_metric[-1]
                  except:
                    try:
                      score_metric.append(parsed_variables[var+".length"])
                      parsed_variables[toset] = score_metric[-1]
                    except:
                      score_metric.append(var)
                      parsed_variables[toset] = score_metric[-1]
                      need_input.append(cur_line)
              if(chk_if_closed(cur+1,line_no,split_content)):
                score_metric.pop()

          match_fnd = re.findall(r'\b(\w+)\s*(==|!=|>|<|>=|<=)\s*(\w+)\b',arg,re.IGNORECASE|re.MULTILINE)
          for fnd in match_fnd:
            toset,op, var = fnd
            if var:
              if var.isnumeric():
                try:
                  score_metric.append(abs(var - parsed_variables[toset]))
                  parsed_variables[toset] = score_metric[-1]
                except:
                  score_metric.append(var)
                  parsed_variables[toset] = score_metric[-1]
              else:
                try:
                  score_metric.append(parsed_variables[var])
                  parsed_variables[toset] = score_metric[-1]
                except:
                  score_metric.append(var)
                  parsed_variables[toset] = score_metric[-1]
                  need_input.append(cur_line)
              if(chk_if_closed(cur+1,line_no,split_content)):
                score_metric.pop()


      fe_matches = re.findall(for_each_chk, cur_line,re.IGNORECASE|re.MULTILINE)
      if len(fe_matches):
        debug_help[cur] = {"line":f"{len(score_metric)}","->":cur_line}
        chk_passed.append(cur)
        for imatch in fe_matches:
          # print(imatch)
          var, it = imatch
          try:
            score_metric.append(parsed_variables[var])
          except:
            try:
              score_metric.append(parsed_containers[var])
            except:
              try:
                score_metric.append(parsed_variables[var+".size()"])
              except:
                try:
                  score_metric.append(parsed_variables[var+".length"])
                except:
                  score_metric.append(var)
                  need_input.append(cur_line)
          if(chk_if_closed(cur+1,line_no,split_content)):
            score_metric.pop()

      if cur not in chk_passed:
        to_spare = to_spare + 1

    if "}" in split_content[cur]:
      to_spare = to_spare - 1
      # print(to_spare)
    while to_spare<0:
      score_metric.pop()
      to_spare = to_spare+1
    cur = cur+1

  replace_dic = {}
  score = 1
  for s in range(len(score_metric)):
    if not score_metric[s].isnumeric():
      try:
        score_metric[s] = replace_dic[score_metric[s]]
        score = score * score_metric[s]
      except:
        print(f"Enter length of: {score_metric[s]}")
        replace_dic[score_metric[s]] = int(input())
        score_metric[s] = replace_dic[score_metric[s]]
        score = score * score_metric[s]
    else:
      score = score * score_metric[s]

  result = {
      "parent_func": parent_func,
      "parent_line": start,
      "parent_args": parent_args,
      "score_metric": score_metric,
      # "debug_help": debug_help,
      "complex_score": score
  }
  return result


def extract_log_info(content):
  logline_catalogue = {}
  logline_index = []
  log_line_info = {}
  space_score = {}
  complex_score = {}
  parent_func_info = {}
  split_content = content.split("\n")
  log_line_reg = r"(LOGGER|LOG|\w*)\.(INFO|debug|error|WARN\w*|log\w*|SEVERE|CONFIG|FINE\w*)(\(.*\))"
  # print(split_content)
  for line_no, line_code in enumerate(split_content):
    log_line_matches = re.findall(log_line_reg, line_code, re.MULTILINE|re.IGNORECASE)
    if len(log_line_matches):
      logline_index.append(line_no)
      for lmatch in log_line_matches:
          variable, log_operation, log_content = lmatch
          logline_catalogue[line_no] = line_code
          log_line_info[line_no] = get_log_state(split_content, line_no)
          parent = log_line_info[line_no]["parent_func"]
          ignore = log_line_info[line_no]["parent_line"]
          s_score = 1
          c_score = 1
          for p in parent:
            parent_func_info[line_no] = extract_log_func(p,content,space_score,ignore)
            s_score = s_score * parent_func_info[line_no]["space_score"]
            c_score = c_score * parent_func_info[line_no]["complex_score"]
          space_score[line_no] = len(log_content) * s_score
          complex_score[line_no] = log_line_info[line_no]["complex_score"] * c_score





  result = {
      "logline_catalogue": logline_catalogue,
      "logline_index": logline_index,
      "log_line_info": log_line_info,
      "space-score": space_score,
      "parent_func_info": parent_func_info,
      "complex-score": complex_score
  }
  return result

result = extract_log_info(content)
for i in result["logline_index"]:
  print(result["logline_catalogue"][i])
  print("space-score:"+str(result["space-score"][i]))
  print("time-score:"+str(result["complex-score"][i]))
  print(result["log_line_info"][i])
  print(result["parent_func_info"][i])

# Demonstrating Approach to find every class data member

import re

def extract_class_data(java_code):
    data_members = {}
    member_functions = {}
    classes = []


    data_member_pattern = r"(?:(?:private|public|protected|static|final|abstract)*\s+)+([\w<>?,\[\]\s]+)\s+(\w+)\s*(=|;)"
    member_function_pattern = r"((private|public|protected|static|final|abstract)\s+)*([\w<>?,\[\]\s]+)\s+(\w+)\s*\(([^)]*)\)\s*\{"

    matches = re.findall(data_member_pattern, java_code)
    for match in matches:
        data_type, data_member, not_req = match
        data_members[data_member] = data_type.strip()


    matches = re.findall(member_function_pattern, java_code)
    for match in matches:
        not_rq1, not_rq2, return_type, member_function, parameters = match
        parameter_list = [param.strip() for param in parameters.split(",")]
        member_functions[member_function] = [return_type.strip(), parameter_list]


    class_pattern = r"(?:(?:private|public|protected|static|final|abstract)\s+)?(?:class|interface)\s+(\w+)\s*\{"
    matches = re.findall(class_pattern, java_code)
    classes = matches


    result = {
        "data_members": data_members,
        "member_functions": member_functions,
        "classes": classes
    }
    return result

java_code = content


class_data = extract_class_data(java_code)
print(class_data)


member_functions_list = list(class_data['member_functions'].keys())
try:
  member_functions_list.remove("for")
except:
  print("")
try:
  member_functions_list.remove("if")
except:
  print("")
member_functions_list

# Demonstration of how classes and functions are identified and what is the line range of them in code

import os
import re

log_regex = r'(LOGGER|LOG|LEVEL)\.(LOGGER|LOG|info|debug|error|warning)'
# class_regex = r"(?:(?:private|public|protected|static|final|abstract)\s+)?(?:class|interface)\s+(\w+)\s*\{"
member_function_pattern = r"((private|public|protected|static|final|abstract)\s+)*([\w<>?,\[\]\s]+)\s+(\w+)\s*\(([^)]*)\)\s*\{"
main_class = file_name.split(".")[0]
print(main_class)
main_dic = {}
line_list = content.split("\n");
line_cnt = enumerate(line_list,1);
log_line_list = []

flag_status = []
function_def_list = {}
braces_status = 0
braces_flag = []
print(line_cnt);
for count, line in line_cnt:
  log_statements = re.findall(log_regex, line, re.MULTILINE|re.IGNORECASE)
  open_func = re.findall(r"\{", line, re.MULTILINE|re.IGNORECASE)
  close_func = re.findall(r"\}", line, re.MULTILINE|re.IGNORECASE)
  # classes = re.findall(class_regex, line, re.MULTILINE|re.IGNORECASE)
  function = re.findall(member_function_pattern, line,  re.MULTILINE|re.IGNORECASE)
  if(len(log_statements)>0):
    log_line = []
    log_line.append(count)
    log_line.append(line)
    log_line_list.append(log_line)
  if(len(close_func)>0):
    braces_status = braces_status - 1
    # print(braces_status)
    if braces_status in braces_flag:
      # print(count)
      # print(braces_flag)
      # print(flag_status)
      function_def_list[flag_status[len(flag_status)-1]].append(count)
      flag_status.pop()
      braces_flag.remove(braces_status)
  if(len(function)>0):
    for match in function:
        not_rq1, not_rq2, return_type, member_function, parameters = match
    if member_function in member_functions_list:
        function_def_list[member_function] = [count]
        braces_flag.append(braces_status)
        flag_status.append(member_function)
        # print(count)
        # print(member_function)
        # print(braces_flag)
        # print(flag_status)
  if(len(open_func)>0):
    braces_status = braces_status + 1
    # print(braces_status)
print(function_def_list)
print(log_line_list)

log_lines = []
for log in log_line_list:
  log_lines.append(log[0])

log_dic = {}
for num in log_lines:
  log_parent_func = []
  for func in member_functions_list:
    if num>=function_def_list[func][0] and num<=function_def_list[func][1]:
      log_parent_func.append(func)

print(log_parent_func)
for val in log_parent_func:
  print(class_data['member_functions'][val][1])




# import re

# def parse_java_code(java_code):
#     func_def_pattern = r"(?:(?:public|protected|private|static|final|\s)+[\w\<\>\[\]]+\s+)+(\w+)\s*\([^\)]*\)\s*(?:throws\s*[\w\.]+\s*)?\{"
#     func_call_pattern = r"(?:(\w+)\s*=\s*)?(\w+)\s*\([^\)]*\);"
#     arg_pattern = r"(\w+)\s+(\w+)(?:\s*=\s*[^,]+)?(?:,|$)"


#     main_func_match = re.search(r"public\s+static\s+void\s+main\s*\(\s*String\[\]\s+(\w+)\s*\)\s*\{", java_code)
#     if not main_func_match:
#         raise ValueError("Main function not found!")

#     main_func_name = main_func_match.group(1)
#     main_func_args = []


#     func_calls = re.findall(func_call_pattern, java_code)

#     print(func_calls)
#     main_func_node = {
#         "name": main_func_name,
#         "return_type": "void",
#         "args": main_func_args,
#         "children": []
#     }

#     for assign_var, func_name in func_calls:
#         func_def_match = re.search(fr"{func_def_pattern}{func_name}\s*\(", java_code)
#         if not func_def_match:
#           return_type = "NA"
#           func_args = "NA"
#           # raise ValueError(f"Function definition not found for {func_name}!")
#           ignore = True

#         if not ignore:
#           func_def = func_def_match.group()
#           func_name, return_type = func_def_match.groups()[1].split()

#           func_args = re.findall(arg_pattern, func_def)
#           func_args = [{"type": arg_type, "name": arg_name} for arg_type, arg_name in func_args]

#         func_call_node = {
#             "name": func_name,
#             "return_type": return_type,
#             "args": func_args,
#             "children": []
#         }

#         main_func_node["children"].append(func_call_node)
#         ignore = False
#     return main_func_node


# java_code = content

# tree = parse_java_code(java_code)
# print(tree)


data_member_pattern = r"(?:(?:private|public|protected|static|final|abstract)*\s+)+([\w<>?,\[\]\s]+)\s+(\w+)\s*(=|;)"

# Demonstration of how for loops are supposed to be converted to number of iterations that we use to calculate log_score

import re

# def execute_python_code_with_user_input(python_code):
#     try:
#         exec(python_code)
#     except NameError as e:
#         var_name = str(e).split("'")[1]
#         user_input = input(f"Enter the value for '{var_name}': ")

#         print(f"{var_name} = {user_input}")

#         try:
#             print(python_code)
#         except Exception as e:
#             print(f"Error: {e}")

def convert_java_loop_to_python_while(java_for_code):
    indent = 0;
    python_while_code = ""
    found = []
    cost = 1
    pattern_for1 = r"for\s*\((.*?);(.*?);(.*?)\)\s*{"
    pattern_for2 = r"for\s*\((.*?):(.*?)\)\s*{"
    matches_for1 = re.findall(pattern_for1, java_for_code,re.MULTILINE|re.IGNORECASE)
    matches_for2 = re.findall(pattern_for2, java_for_code,re.MULTILINE|re.IGNORECASE)

    if len(matches_for1):
      init_statement, condition, update_statement = matches_for1[0]
      init_statement = init_statement.replace("int", "").strip()
      condition = condition.replace(";", "").strip()
      if update_statement[-1] == update_statement[-2]:
        update_statement = update_statement[:-1]
        update_statement+="=1"
      python_while_code = f"{init_statement}\n"
      python_while_code += f"\t"*indent+f"while {condition}:"
      python_while_code += f"\n    {update_statement}"
      try:
        exec(python_while_code)
      except NameError as e:
          flag = True
          var_name = str(e).split("'")[1]
          user_input = input(f"Enter the value for '{var_name}': ")
          python_while_code = f"{var_name} = {user_input}\n" + python_while_code
          try:
            print(python_while_code)
            # cost = cost * exec(python_while_code)
          except Exception as e:
            print(f"Error: {e}")

    if len(matches_for2):
      iterator, limit = matches_for2[0]
      iterator = iterator.strip().split(" ")[-1]
      limit = limit.strip()
      if limit not in found:
        user_input = input(f"Enter the size for '{limit}': ")
        found.append(limit)
        cost = cost * user_input
    print(cost)

java_for_loop_code = "for (int i = n; i > m; i--) {"
java_for_loop_code += "\n  for(int j:arr){}"
java_for_loop_code += "\n    // Your code here"
java_for_loop_code += "\n}"

python_while_loop_code = convert_java_loop_to_python_while(java_for_loop_code)








# Example usage:
python_code = """
# Some Python code that uses a variable 'x'
print(x + 10)
"""

execute_python_code_with_user_input(python_code)








import re
match_argument =  r"(.\w+)\s*\((.+)\)\s*({)"
match_forEach = r"(.\w+)\.forEach\s*\(\s*\((\w+)\)\s*->\s*({|)"

# example = "for(int i=0;i<arr;i++){"
# example ="for(int i:arr){"
example = "while (i<arr) "
# example = "while (crunchifyIterator.hasNext()){"
# example = "crunchifyList.forEach((temp) -> {"

matches = re.findall(match_argument, example,re.MULTILINE|re.IGNORECASE)
forEachmatch = re.findall(match_forEach, example,re.MULTILINE|re.IGNORECASE)
if len(matches):
  structure, argument, closing = matches[0]
  print(f"{structure},argument: {argument}, {closing}")
if len(forEachmatch):
  argument, iterator, closing = forEachmatch[0]
  print(f"forEach,argument: {iterator} in {argument}, {closing}")

# if len(argument):
#   init_statement, condition, update_statement = argument.split(";")
#   init_statement = init_statement.replace("int", "").strip()
#   condition = condition.replace(";", "").strip()
#   if update_statement[-1] == update_statement[-2]:
#     update_statement = update_statement[:-1]
#     update_statement+="=1"
#   python_while_code = f"{init_statement}\n"
#   python_while_code += f"\t"*indent+f"while {condition}:"
#   python_while_code += f"\n    {update_statement}"
#   try:
#     exec(python_while_code)
#   except NameError as e:
#       flag = True
#       var_name = str(e).split("'")[1]
#       user_input = input(f"Enter the value for '{var_name}': ")
#       python_while_code = f"{var_name} = {user_input}\n" + python_while_code
#       try:
#         print(python_while_code)
#         # cost = cost * exec(python_while_code)
#       except Exception as e:
#         print(f"Error: {e}")

# Implementing variable storage and updates calculation and storage to avoid redundancy of asking users for information to calculate number of iterations



import re

def evaluate_operation(operation, variable_dict):
  for var, value in variable_dict.items():
    operation = re.sub(r'\b' + re.escape(var) + r'\b', str(value), operation)
    # print(operation)
  try:
    return eval(operation)
  except:
    return operation

def parse_java_code(java_code):
  variable_dict = {}
  cont_dict = {}
  assignment_regex = r'(\w+)\s*=\s*([^<>]*)\s*;'
  array_regex = r'(\w+[\[\]]+)\s*=\s*([^<>=]*)\s*;'
  b_array_regex = r'\s*.*(\[\]\s*\w|\w+\[\]).*=(\s*.*);'
  unary_operator_handler = r'((\w)\s*([+\-*/%]))\s*=(.*)'
  clone_regex = r'=(.*\.(copy.*|clone.*)\((.*)\)).*'
  col_regex = r'\<.*\>\s*(\w+)=\s*(.*);'
  itr_regex = r'(\w+)\s*=\s*(\w+)\..*iterator.*'
  lines = java_code.split("\n")

  for line in lines:
    line = line.replace("++","+=1")
    line = line.replace("--","+=1")
    unary_matches = re.findall(unary_operator_handler, line,re.IGNORECASE|re.MULTILINE)
    if len(unary_matches):
      for found_match in unary_matches:
        # print(found_match)
        to_replace, var, operator, value = found_match
        line = re.sub(r'\b' + re.escape(to_replace), var, line)
        line = re.sub(r'\b' + re.escape(value)  , var+operator+value, line)
    # print(line)


    col_matches = re.findall(col_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(col_matches):
      for cmatch in col_matches:
        # print(cmatch)
        variable, size = cmatch
        numbers = re.findall(r'\((\d+)\)',size)
        # print(numbers)
        if len(numbers):
          size = int(numbers[0])
          cont_dict[variable] = size
          variable_dict[variable+'.size()'] = size
        else:
          cont_dict[variable] = size

    clone_matches = re.findall(clone_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(clone_matches):
      for cmatch in clone_matches:
        # print(cmatch)
        to_replace, func, value = cmatch
        numbers = re.findall(r'\d+',value)
        # print(numbers)
        if len(numbers):
          size = numbers[0]
          for i in range(1,len(numbers)):
            size = abs(numbers[i]-size)
          # print(size)
          line = re.sub(r'' + re.escape(to_replace), size, line)
          # print(line)
        else:
          line = re.sub(r'' + re.escape(to_replace), value, line)


    array_matches = re.findall(b_array_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(array_matches):
      for amatch in array_matches:
        # print(amatch)
        variable, size = amatch
        numbers = re.findall(r'\[(\d+)\]',size)
        # print(numbers)
        if len(numbers):
          size = int(numbers[0])
          for i in range(1,len(numbers)):
            size = abs(int(numbers[i])*size)
          # print(size)
          variable = variable.replace("[","")
          variable = variable.replace("]","")
          cont_dict[variable] = size
          variable_dict[variable+'.length'] = size
        else:
          variable = variable.replace("[","")
          variable = variable.replace("]","")
          cont_dict[variable] = size
          variable_dict[variable+'.length'] = size


    assignment_match = re.findall(assignment_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(assignment_match):
      variable_name, variable_value = assignment_match[0]
      # print(f"variable_name:{variable_name} variable_value:{variable_value}")

      evaluated_value = evaluate_operation(variable_value, variable_dict)
      if evaluated_value is not None:
        variable_dict[variable_name] = evaluated_value
      else:
        variable_dict[variable_name] = variable_value


    itr_matches = re.findall(itr_regex, line,re.IGNORECASE|re.MULTILINE)
    if len(itr_matches):
      for imatch in itr_matches:
        print(imatch)
        variable, size = imatch
        try:
          size=cont_dict[size]
        except:
          try:
            size=variable_dict[size+".size()"]
          except:
            size =size

        variable_dict[variable] = size

    for var in variable_dict.keys():
      try:
        variable_dict[var] = evaluate_operation(variable_dict[var], variable_dict)
        variable_dict[var] = cont_dict[variable_dict[var]]
        variable_dict[var] = evaluate_operation(variable_dict[var], container_dict)
      except:
        continue

  return variable_dict, cont_dict

# Example Java code
java_code = '''
int x = n;
String s = "Abu";
int[][] a = new int[5][10];
int c[] = new int[10];
int b[] = Arrays.copyOf(a);
HashMap<Integer, Integer> map= new HashMap<>(10);
x++;
int y = 10;
y++;
int z = x + y;
x = x * 2;
int n = 2;
for(int i=x; i<n;i++){
  //loop
}
Iterator<Integer> m = map.iterator();
ListIterator<String> crunchifyListIterator = crunchifyList.listIterator();
'''

parsed_variables, parsed_containers = parse_java_code(java_code)
print(parsed_variables)
print(parsed_containers)


