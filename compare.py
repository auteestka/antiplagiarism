import argparse
import numpy as np

def LDistance(string1,string2):
  '''
  Levenshtein distance
  '''
  n, m = len(string1), len(string2)
  D = np.zeros((n+1, m+1))
  for i in range(n+1):
    for j in range(m+1):
      if i==0:
        D[i,j]=j
      elif j==0:
        D[i,j]=i
      else:
        D[i,j]=min(D[i-1,j]+1, D[i,j-1]+1, D[i-1,j-1]+1-(string1[i-1]==string2[j-1]))
  return D[n,m]


def preprocessing(path):
  '''
  This function deletes all comments, spaces and \n 
  and converts residual into one string. This approach is quite normal since 
  we do not want to take expressions like ')' as individual tokens. 
  The better approach would be to use some tree structure upon the code, but 
  the distance between graphs is quite complicated so I will choose one-string way for now.
  '''
  cleanCode = ''
  f_length  = 0
  triple_quotes = False
  with open(path, 'r') as f:
    for line in f:
      f_length += len(line)+1
      line = line.replace('\n','').replace(' ','') # delete \n and spaces within one line
      if triple_quotes:                            # delete triple quotes
        if "'''" in line:
          line = line[line.find("'''")+3:]
          triple_quotes = False
        else:
          continue
      else:
        if "'''" in line:
          line = line[:line.find("'''")]
          triple_quotes = True
      if '#' in line:
        line = line[:line.find('#')]               # delete comments
      if line:
        cleanCode += line.lower()                  # lower case we need

  return cleanCode, f_length-1


# 'main' function
parser = argparse.ArgumentParser(description='pairs to scores')
parser.add_argument('pairs', type=str)
parser.add_argument('scores', type=str)
args = parser.parse_args()

with open(args.pairs, 'r') as f:
  with open(args.scores, 'w') as w:
    for pair in f:
      path1, path2  = pair.split()
      string1, len1 = preprocessing(path1)
      string2, len2 = preprocessing(path2)
      l_dist = LDistance(string1, string2)
      score  = 1 - l_dist * 2/(len1+len2)         # Levenshtein distance -> Score
      w.write(str(score)+'\n')
