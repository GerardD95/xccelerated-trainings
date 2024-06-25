## cpython

| rows          | first: inplace updates | second: multi processing | second: chunk_size | third             | third: chunk_size | optimized? |     |
| ------------- | ---------------------- | ------------------------ | ------------------ | ----------------- | ----------------- | ---------- | --- |
| 10_000        | 0.04047925001941621    | 0.15702120796777308      | 100_000            |                   |                   | yes        |     |
| 100_000       | 0.11770470801275223    | 0.24337337503675371      | 100_000            |                   |                   | yes        |     |
| 1_000_000     | 0.9273274169536307     | 0.5364997499855235       | 100_000            |                   |                   | yes        |     |
| 10_000_000    | 8.797820500098169      | 3.59368400007952         | 500_000            |                   |                   | yes        |     |
| 40_000_000    | 36.01542679197155      | 18.903227958013304       | 700_000            | 9.999033374944702 | 700_000           | not yet    |     |
| 100_000_000   | 89.36997662496287      | 69.07721608399879        | 10_000_000         | 24.24181795795448 | 10_000_000        | yes        |     |
| 1_000_000_000 |                        |                          |                    |                   |                   |            |     |
## pypy

| rows          | first: inplace updates | second: multi processing | second: chunk_size | third             | third: chunk_size | optimized? |     |
| ------------- | ---------------------- | ------------------------ | ------------------ | ----------------- | ----------------- | ---------- | --- |
| 10_000        | 0.04047925001941621    | 0.15702120796777308      | 100_000            |                   |                   | yes        |     |
| 100_000       | 0.11770470801275223    | 0.24337337503675371      | 100_000            |                   |                   | yes        |     |
| 1_000_000     | 0.9273274169536307     | 0.5364997499855235       | 100_000            |                   |                   | yes        |     |
| 10_000_000    | 8.797820500098169      | 3.59368400007952         | 500_000            |                   |                   | yes        |     |
| 40_000_000    | 36.01542679197155      | 18.903227958013304       | 700_000            | 9.999033374944702 | 700_000           | not yet    |     |
| 100_000_000   | 89.36997662496287      | 69.07721608399879        | 10_000_000         | 24.24181795795448 | 10_000_000        | yes        |     |
| 1_000_000_000 |                        |                          |                    |                   |                   |            |     |

## Improvements
- Rolling values rather than calculating after
- Dict lookup slow(ish)
- Append sucks (performance wise)
- Readline goes over each char
- Split goes over each char
- Read as ascii rather than unicode
- Parallelism?
- partitioning of chunks 
- stop splitting after the first occurance of ;
- read as rb instead of decoding directly?
- replace CityStats class
- split file by file size