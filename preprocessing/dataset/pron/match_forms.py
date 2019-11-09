#!/usr/bin/env python3
# CS 221
# Andrew Yang

# Code and phonological data adapted from https://en.wiktionary.org/wiki/Module:ltc-pron

from util_ltc import load_resources
import fileinput, re, json, sys

resources = None
char_map = {}
scholars = [
  'Zhengzhang',
  'Pan',
  'Shao',
  'Pulleyblank',
  'Li',
  'Wang',
  'Karlgren'
]

def infer_categories(text):
  t = [c for c in text]
  initial, final, deng, openness, tone = t[0], t[1], t[2], t[3], t[5]
  if re.search('-', text):
    deng = text.split('-')[1] + deng
  if tone == '入' and final in resources['fin_conv']:
    final = resources['fin_conv'][final]
  initial_type = resources['init_type'][initial]
  tone_label = resources['tone_class'][tone]
  if re.match(resources['final_type_1'], final):
    final_type = resources['fin_type_open'][final + openness]
  elif re.match(resources['final_type_2'], final):
    final_type = resources['final_deng'][final + deng]
  elif re.match(resources['final_type_3'], final):
    final_type = resources['fin_type_deng_open'][final + deng + openness]
  elif re.match(resources['final_type_4'], final):
    if deng == '重鈕三':
      final_type = resources['final_openness'][final + openness]
    else:
      final_type = resources['final_deng'][final + deng]
  elif re.match(resources['final_type_5'], final):
    final_type = resources['fin_type'][final]
  else:
    raise ValueError('Final not recognized')
  return initial_type, final_type, tone_label

def reconstruct_from_table(char_idx, initial, final):
  for name in scholars:
    initial_conv = resources['initialConv'][name][initial]
    final_conv = resources['finalConv'][name][final]
    char_map[char_idx][name] = {
      'initial': initial_conv,
      'final': final_conv
    }

def main():
  global resources
  global char_map

  resources = load_resources()
  for line in fileinput.input():
    ln = line.strip().split(',')
    char_idx = ln[0] + ln[1]
    initial, final, tone_label = infer_categories(ln[2][1:-1])

    assert char_idx not in char_map
    char_map[char_idx] = {'tone_label': tone_label}
    reconstruct_from_table(char_idx, initial, final)

  json.dump(
    char_map,
    fp=sys.stdout,
    ensure_ascii=False
  )

if __name__ == "__main__":
  main()