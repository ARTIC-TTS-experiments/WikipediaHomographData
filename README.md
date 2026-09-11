# Homograph disambiguation data

This repository provides labeled data for training homograph disambiguation
models, as described in:

Tihelka, D., Tihelková, A., Řezáčková, M., and Matoušek, J. (2026). [Text-to-Text Transfer
Transformer as a High-Precision Homograph Disambiguator] (under review)

The data are fork of the original repository https://github.com/google-research-datasets/WikipediaHomographData
(commit 8f008f021e88f8b71118a27ae655f1f3121162bc), and contain the
fixes described in the above mentioned paper. Also, they contain the additional
homograph words in cases where there are multiple such words in a sentence.


The original repository was described in paper:

Gorman, K., Mazovetskiy, G., and Nikolaev, V. (2018). [Improving homograph
disambiguation with machine
learning](https://www.aclweb.org/anthology/L18-1215/). In 
_Proceedings of the Eleventh International Conference on Language Resources
and Evaluation_, pages 1349-1352. Miyazaki, Japan.

If you use this data in a publication, we would appreciate if you cite this
paper.

## Annotation

Sentences were extracted from English Wikipedia articles. Homograph were
initially labeled for the most likely `WORDID` (as defined below) in context by
a team of three annotators. In the case that all three did not agree on the
`WORDID`, a fourth senior annotator resolved the disagreements.

There are now 162 unique homographs and roughly 100 examples per homograph.

## Organization

The files `data/train.tsv` and `data/eval.tsv` are TSV files with
the following fields:

* `sentence`: text of the example with the homograph word surrounded by <> for
    the original homograph word, and by <<>> for the other homograph words, if
    there are such in the sentence
* `wordid`: name of the pronunciation (homograph variant), related to the homograph
    word surrounded by <>
* `wordid2`: name of the pronunciation (homograph variant) of the second homograph,
    the first in the sentence surrounded by <<>>
* more `wordidX` may follow, if there are multiple homograph words in
   the sentence. They are ordered by their position, though.

These two files represent a suggested 90%/10% train/test split stratified by
homograph.

In this repository, the "new" format is used, which is more suitable for the annotation
of multiple homograph words. If the original format of the dataset is preferred (with
the fixes included), it can be obtained from `orig_format` branch.


The file `data/wordids.tsv` is a TSV file which maps from the `WORDID` field
above to information used by the annotator: -a short human-readable description
of the `WORDID`, and a transcription of the `WORDID`. Note that neither are 
intended to be authoritative; they are simply to help users distinguish between
the various `WORDID`s for a homograph. The final two fields have some
impressionistic taxonomic information about the nature of the homography itself
intended for use during error analysis. The following fields are present:

* `homograph`: the homograph word itself
* `wordid`: name of the pronunciation
* `label`: a short human-readable description of the `wordid`
* `pronunciation`: a phonemic transcription of the `wordid` in US English.
* `homograph_type`: a binary category describing the broad source of
  homography: morphosyntactic derivations from the same lemma, or lexically
  distinct terms.
* `fine_homography_type`: a more detailed classification of the above.

## Authors

The original data was collected by [Kyle Gorman](mailto:kbg@google.com),
[Vitaly Nikolaev](mailto:vitalyn@google.com), and
[Gleb Mazovetskiy](mailto:glebm@google.com), with help from a team of linguists
and annotators.

The fixes and multiple homograph annotations were added by
[Daniel Tihelka](mailto:dtihelka@fav.zcu.cz),
[Alice Tihelková](mailto:atiheko@ff.zcu.cz),
[Markéta Řezáčková](mailto:juzova@fav.zcu.cz), and
[Jindřich Matoušek](mailto:jmatouse@fav.zcu.cz),

## License

See `LICENSE`.

## Contributing

See `CONTRIBUTING`.

## Mandatory disclaimer

This is not an official Google product.
