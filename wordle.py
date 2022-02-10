from collections import defaultdict
import sys

allowed_guesses = open('allowed_guesses.txt').read().splitlines()
answers = open('answers.txt').read().splitlines()
guesses_set = set(allowed_guesses).union(set(answers))
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
all_letters = set(LETTERS)
auto = len(sys.argv) == 2 and sys.argv[1] == '--auto'

class WordleWord:
  def __init__(self, word, contained_indices=[], correct_indices=[]):
    self.word = word
    contained_dict = defaultdict(set)
    for i in contained_indices + correct_indices:
      ch = word[i]
      contained_dict[ch].update([i for i, c in enumerate(word) if c == ch])
    self.meta = []

    for i, c in enumerate(self.word):
      self.meta.append({
        'correct_pos': i in correct_indices,
        'char_in_word': c in contained_dict,
        'letter': c,
        'index': i
      })

    bad_indexes = list(set([0, 1, 2, 3, 4]) - set([item for sublist in contained_dict.values() for item in sublist]))
    self.bad_letters = [self.word[c] for c in bad_indexes]

  def get_word(self):
    return self.word
  
  def get_meta(self):
    return self.meta

  def get_bad_letters(self):
    return self.bad_letters

def checker(words_used = []):
  chars_left = all_letters
  valid_letters = [all_letters] * 5
  required_letters = set()
  for word in words_used:
    meta = word.get_meta()
    bad_letters = word.get_bad_letters()
    chars_left -= set(bad_letters)
    for i in range(len(valid_letters)):
      valid_letters[i] = valid_letters[i].intersection(chars_left)
    for ch in meta:
      ch_index = ch['index']
      c_set = set([ch['letter']])
      if ch['correct_pos']:
        valid_letters[ch_index] = c_set
      elif ch['char_in_word']:
        # char is in word, but wrong location. remove letter from current index
        valid_letters[ch_index] -= c_set

      if ch['char_in_word']:
        required_letters = required_letters.union(c_set)

  res = []
  for word in answers:
    contains_required = len(required_letters - set(word)) == 0
    
    if len(required_letters) > 0 and not contains_required:
      continue

    match = True
    for i, c in enumerate(list(word)):
      if c not in valid_letters[i]:
        match = False
    if match:
      res.append(word)
  
  return res

def convert_input(s):
  return [int(x) - 1 for x in s.replace(' ', '').replace(',', '') if x]

def get_index_input(prompt):
  res = []
  while min(res, default=-1) < 0 or max(res, default=6) > 4:
    try:
      res = convert_input(input(prompt))
      if len(res) == 0:
        break
    except ValueError:
      res = []
  return res

def main():
  words_used = []
  possible_words = allowed_guesses[:1]

  for _ in range(6):
    word = ''
    if auto and len(possible_words):
      word = possible_words[0]
      print('Enter valid word:', word)
    else:
      while len(word) != 5 or word not in guesses_set:
        word = input('Enter valid word: ')
    yellow_indices = get_index_input('Enter yellow positions (1-5) separate by comma (e.g. 1,2,3,4,5): ')
    green_indices = get_index_input('Enter green positions (1-5) separate by comma (e.g. 1,2,3,4,5): ')

    words_used.append(WordleWord(word, yellow_indices, green_indices))
    possible_words = checker(words_used)
    res = ', '.join(possible_words)
    if len(possible_words) == 1:
      print('Your word is' , res)
      break
    else:
      print('Possible words:', res)

if __name__ == "__main__":
  try:
    main()
  except:
    pass