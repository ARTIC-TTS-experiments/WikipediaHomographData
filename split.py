
import argparse
import re
import os.path
import sys

# --------------
def read_homographs(fname:str) :
    '''
    Reads a TSV file containing homograph data (in new format).
    and strips quotes/headers.

    Args:
        fname (str): The path to the input TSV file.

    Returns:
        list[list[bytes]]: A list of rows (excluding the header row), where
            each row is represented as a list of cleaned byte strings representing
            the tab-separated fields. The first field is the sentence, next fields
            are homograph IDs.
    '''
    with open(fname, 'rt') as f :
         data = f.readlines()
         data = [d.encode('utf8').split(b'\t') for d in data]
         # Store the data to buffer
         for i,d in enumerate(data) :
             data[i] = [x.strip().removeprefix(b'"').removesuffix(b'"').replace(b'""', b'"') for x in d]
    # Get the data, without the header
    return data[1:]

# -------------
def conv_homographs(input:str, out_dir:str, all_homographs:bool) :
    '''
    Converts homograph corpus data from the new format into the original format.

    Parses marked homographs (<...> or <<...>>) from sentences, cleans markup tags,
    recalculates word start/end character offsets, and exports the data into individual
    TSV files per homograph inside the designated output directory.

    Args:
        input (str):           Path to the raw input dataset TSV file.
        out_dir (str):         Directory where output TSV files named after each homograph
                               will be saved.
        all_homographs (bool): If True, processes all homographs including secondary ones
                               marked with double angle brackets (<<...>>). If False,
                               processes only primary homographs marked with single angle
                               brackets (<...>).
    '''

    class Item :
          '''
          Auxiliary class holding the data of a homograph word.
          '''

          def __init__(self, h:str,w:str,s:str,b:int,e:int) :
              self.__h = h
              self.__w = w
              self.__s = s
              self.__b = b
              self.__e = e

          def sent(self, s:str) :
              self.__s = s

          def shift(self, v:int) :
              self.__b += v
              self.__e += v

          @property
          def start(self) :
              return self.__b
          @property
          def end(self) :
              return self.__e
          @property
          def data(self) :
              return (self.__h,
                      self.__w,
                      self.__s,
                      self.__b,
                      self.__e,
                     )
          @staticmethod
          def header() :
              return Item(b'homograph',
                          b'wordid',
                          b'sentence',
                          b'start',
                          b'end',
                         )


    # Homograph word parser
    hwords1 = re.compile(b'(^|[^<])<([^<>]+)>([^>]|$)')
    hwordsM = re.compile(b'([<]+)([^<>]+)([>]+)')
    words   = {}
    # Which word to handle? Orig or all?
    homogr  = hwordsM if all_homographs else hwords1

    # Read the file and process the items
    for S,*data in read_homographs(input) :

        # Auxiliary storage for post processing
        X = []
        # Get the homograph world(s)
        for h in homogr.finditer(S) :
            W   = h.group(2)
            w   = W.lower()
            # Get the position in the sentence (with <> marked homographs)
            b,e = h.span(2)
            # Get the type - the original word first (<>), remaining start at index 1 (<<>>)
            x   = data[0] if b'<<' not in h.group(1) else data.pop(1)

            # Create data item
            D   = words.setdefault(w, [Item.header(), ])
            # Add the current word
            D.append(Item(w,x,S,b,e))
            # Store it for further processing
            X.append(D[-1])

        # And post process the data by removing < in the sentences
        while h := hwordsM.search(S) :

            W   =  h.group(2)
            B,E =  h.span(0)
            W,Y =  h.span(2)

            # Update sentence
            s   =  S
            S   =  S[:B] + S[W:Y] + S[E:]

            # Propagate the changes to all stored sentences
            for x in X :
                # Change the sentence
                x.sent(S)
                # Whole before the match - ignore
                if   x.end < W :
                     continue
                # Whole after the match - shift for bots < and >
                elif x.start > Y :
                     x.shift(-W+B - E+Y)
                # Shift just only for <
                else  :
                     x.shift(-W+B)


    # Store words to the files
    for h,sents in words.items() :
        h = h.decode('utf8').replace('"', '')

        # Store to word-file
        with open(os.path.join(out_dir, f'{h}.tsv'), 'wb') as f :
             for s in sents :
                 #
                 s   = [(b'"' + x.replace(b'"', b'""') + b'"') if isinstance(x,bytes) else str(x).encode('utf8') for x in s.data]
                 # Store
                 f.write(b'\t'.join(s))
                 f.write(b'\n')



# -------------
if __name__ == '__main__' :

   # Prepare arguments
   args = argparse.ArgumentParser(description = 'Simple tool converting the new format of WHD corpus '
                                                'to its original format')
   args.add_argument('--out-dir',        default = None,
                     help = 'The path to the directory into which the data in the original format are '
                            'stored. Under this directory, subdirectory based on the name of the input '
                            'file is created (default: data/train/ for train.tsv passed as input)')
   args.add_argument('--all-homographs', default = False, action = 'store_true',
                     help = 'By default, only the original homographs (i.e. these in <...>) are '
                            'processed. If this option is set, all homographs (i.e. also these in '
                            '<<...>>) are included in the output files (default: %(default)s).')
   args.add_argument('input', nargs = 1)

   # Parse arguments
   args = args.parse_args()


   # Single file is supported
   args.input = args.input[0]

   # Resolve undefined
   if not args.out_dir :
      input = os.path.basename(args.input)
      input = os.path.splitext(input)[0]
      # Output dir
      args.out_dir = os.path.join('data', input)

   # Create the output directory
   if not os.path.isdir(args.out_dir) :
       print(f'Creating output directory: {args.out_dir}', file = sys.stderr)
       os.makedirs(args.out_dir)

   # Convert the file
   conv_homographs(args.input, args.out_dir, args.all_homographs)
