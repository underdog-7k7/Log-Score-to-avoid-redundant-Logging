from google.colab import files
file_up = files.upload()

from zipfile import ZipFile
file_name = "chatgpt-java-main.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

# import os

# directory = "Java-Logging-Example-master"

# for filename in os.listdir(directory):
#     file_path = os.path.join(directory, filename)
#     print(file_path)
#     if os.path.isfile(file_path):
#         print(f"File: {filename}")
#     else:
#         print(f"Directory: {filename}")

# import os

# def make_tree(path, level=0):
#     tree = []
#     for item in os.listdir(path):
#         item_path = os.path.join(path, item)
#         if os.path.isdir(item_path):
#             tree.append((level+1, item))
#             sub_tree = make_tree(item_path, level + 1)
#             tree.extend(sub_tree)
#         else:
#             tree.append((level, item))
#     return tree


# root_path = "Java-Logging-Example-master"
# tree = make_tree(root_path)


# for level, item in tree:
#     print("  " * level + item)


java_files_dic = {}
java_files_list = []
import os
import re

logger_regex = r'logger'
log_regex = r'(LOGGER|LOG)(\.*?).(info|debug|error|warning)\((\"r?(.*?)\"(,|\+)(.*?)|\"(.*?)\")\)'
log_func = r'(LOGGER|LOG)(\.*?).(info|debug|error|warning)\((.*?\(.*?\))\)'
def make_tree(path, level=0):
    tree = []
    java_files = False
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.endswith('.java'):
            java_files = True
            tree.append((level + 1, item))
            java_files_dic[item] = (os.path.join(path, item))
            java_files_list.append(item)
        elif os.path.isdir(item_path):
            sub_tree = make_tree(item_path, level + 1)
            if sub_tree:
                tree.append((level + 1, item))
                tree.extend(sub_tree)
                java_files = False
    # if java_files:
    #     tree.insert(0, (level, os.path.basename(path)))
    return tree



root_path = "chatgpt-java-main"
tree = make_tree(root_path)

# For debug
for level, item in tree:
    print("  " * level + item)
    if item in java_files_list:
      print("  " * level +"File:", item)
      path = java_files_dic[item]
      with open(path, "r") as file:
          chknxt = True
          ctr = 0
          control_structures = []
          log_score = []
          import_lines = []
          inheritence_score = 0
          local_pkg = []
          nesting_lvl = 0
          content = file.read()
          code_lines = content.split("\n");
          for line in code_lines:
            if not chknxt and ctr == 1:
              chknxt = True
              ctr = 0
            elif not chknxt and ctr == 0:
              ctr = 1
            if "import" in line:
              for j in java_files_list:
                find = j.split(".java")
                if find[0] in line:
                  local_pkg.append(find[0])
              inheritence_score+=1
              import_lines.append(line)
            if "if" in line and "{" in line:
              control_structures.append("if")
              log_score.append(1)
              chknxt = True
            elif "if" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("if")
              log_score.append(1)
              chknxt = False
            elif "else" in line and "{" in line:
              control_structures.append("else")
              log_score.append(1)
              chknxt = True
            elif "else" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("else")
              log_score.append(1)
              chknxt = False
            elif "for" in line and "{" in line:
              control_structures.append("for")
              log_score.append(int(input("Enter tentative number of time that this loop:\n"+line+"will execute:")))
              chknxt = True
            elif "for" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("for")
              log_score.append(int(input("Enter tentative number of time that this loop:\n"+line+code_lines[code_lines.index(line)+1]+"will execute:")))
              chknxt = False
            elif "try" in line and "{" in line:
              control_structures.append("try")
              log_score.append(1)
              chknxt = True
            elif "try" in line and  "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("try")
              log_score.append(1)
              chknxt = False
            elif "catch" in line and "{" in line:
              control_structures.append("catch")
              log_score.append(1)
              chknxt = True
            elif "catch" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("catch")
              log_score.append(1)
              chknxt = False
            elif "switch" in line and "{" in line:
              control_structures.append("switch")
              log_score.append(1)
              chknxt = True
            elif "switch" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("switch")
              log_score.append(1)
              chknxt = False
            elif "while" in line and "{" in line:
              control_structures.append("while")
              log_score.append(int(input("Enter tentative number of time that this loop:\n"+line+"will execute:")))
              chknxt = True
            elif "while" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("while")
              log_score.append(int(input("Enter tentative number of time that this loop:\n"+line+code_lines[code_lines.index(line)+1]+"will execute:")))
              chknxt = False
            elif "while" in line and "}" in line:
              control_structures.append("do")
              log_score.append(int(input("Enter tentative number of time that this loop:\n"+line+"will execute:")))
              chknxt = True
            elif "while" in line and "}" in code_lines[code_lines.index(line)-1]:
              control_structures.append("do while")
              log_score.append(int(input("Enter tentative number of time that this loop:\n"+line+code_lines[code_lines.index(line)+1]+"will execute:")))
              chknxt = False
            elif "public" in line and "{" in line:
              control_structures.append("class/function")
              log_score.append(1)
              chknxt = True
            elif "public" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("class/function")
              log_score.append(1)
              chknxt = False
            elif "private" in line and "{" in line:
              control_structures.append("class/function")
              log_score.append(1)
              chknxt = True
            elif "private" in line and  "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("class/function")
              log_score.append(1)
              chknxt = False
            elif "protected" in line and "{" in line:
              control_structures.append("class/function")
              log_score.append(1)
              chknxt = True
            elif "protected" in line and "{" in code_lines[code_lines.index(line)+1]:
              control_structures.append("class/function")
              log_score.append(1)
              chknxt = False
            elif chknxt and "{" in line:
              control_structures.append("function")
              log_score.append(1)
              chknxt = True
            if "{" in line:
              nesting_lvl+=1
            if "}" in line:
              nesting_lvl-=1
              try:
                control_structures.pop()
                log_score.pop()
              except:
                print("")
            logger_search =  re.findall(logger_regex, line, re.MULTILINE|re.IGNORECASE)
            if(len(logger_search)>0):
              for statement in logger_search:
                print("  " * level +"LOGGER DEFINITION:", line)
                print("  " * level +"=============================")
            log_statements = re.findall(log_func, line, re.MULTILINE|re.IGNORECASE)
            if(len(log_statements)>0):
              for statement in log_statements:
                print("  " * level +"Log code:", line)
                print("  " * level +"-----------------------------")
                while len(control_structures) < nesting_lvl:
                  chk = code_lines[temp_idx-1]
                  temp_idx = temp_idx - 1
                  control_structures.append(chk.split(" ")[0])
                print("  " * level +"Control structures:", control_structures)
                print("  " * level +"Loop value:", log_score)
                final_score = 1
                for score in log_score:
                  final_score = final_score*score
                print("  " * level +"Log score:", final_score)
                # print("  " * level +"Inheritence number:", inheritence_score)
                # print("  " * level +"Nesting Level:", nesting_lvl)
                print("  " * level +"Log Level:", statement[2])
                if statement[3]:
                  print("  " * level +"Function called:", statement[3])
                print("  " * level +"-----------------------------")
            else:
              log_statements = re.findall(log_regex, line, re.MULTILINE|re.IGNORECASE)
              for statement in log_statements:
                print("  " * level +"Log code:", line)
                print("  " * level +"-----------------------------")
                temp_idx = code_lines.index(line)
                while len(control_structures) < nesting_lvl:
                  chk = code_lines[temp_idx-1]
                  temp_idx = temp_idx - 1
                  control_structures.append(chk.split(" ")[0])

                print("  " * level +"Control structures:", control_structures)
                print("  " * level +"Loop value:", log_score)
                final_score = 1
                for score in log_score:
                  final_score = final_score*score
                print("  " * level +"Log score:", final_score)
                # print("  " * level +"Local Package Inherited:", local_pkg)
                # print("  " * level +"Inheritence number:", inheritence_score)
                # print("  " * level +"Nesting Level:", nesting_lvl)
                print("  " * level +"Log Level:", statement[2])
                if statement[7]:
                  print("  " * level +"Message:", statement[7])
                elif statement[4]:
                  print("  " * level +"Message:", statement[4])
                  if statement[6]:
                    print("  " * level +"Variable:", statement[6])
                print("  " * level +"-----------------------------")
          print("  " * level +"Number of lines:", len(code_lines))


print(java_files_list)


# import re
# # import_regex = r"import.*;$"
# log_regex = r'(LOGGER|LOG)(\.*?).(info|debug|error|warning)\((\"r?(.*?)\"(,|\+)(.*?)|\"(.*?)\")\)'
# log_func = r'(LOGGER|LOG)(\.*?).(info|debug|error|warning)\((.*?\(.*?\))\)'
# for java_file in java_files_list:
#   print("File:", java_file)
#   path = java_files_dic[java_file]
#   with open(path, "r") as file:
#       content = file.read()
#       code_lines = content.split("\n");
#       for line in code_lines:
#         log_statements = re.findall(log_regex, line, re.MULTILINE|re.IGNORECASE)
#         for statement in log_statements:
#           print("Log code:", line)
#           print("-----------------------------")
#           print("Log Level:", statement[2])
#           if statement[7]:
#             print("Message:", statement[7])
#           elif statement[4]:
#             print("Message:", statement[4])
#             if statement[6]:
#               print("Variable:", statement[6])
#           print("-----------------------------")
#         log_statements = re.findall(log_func, line, re.MULTILINE|re.IGNORECASE)
#         for statement in log_statements:
#           print("Log code:", line)
#           print("-----------------------------")
#           print("Log Level:", statement[2])
#           if statement[3]:
#             print("Function called:", statement[3])
#           print("-----------------------------")

