# [MergerMH](/contracts/MergerMH.sol) - first drop merger contract

Merger contract is used to *merge* 2 tokens of the same event
from first drop (see [FairXYZMH](./FairXYZMH.md)) into one token of next level.

This contract also gives rewards for levels, starting from 2nd
(i.e. for merging 4 or more tokens of 0th level from the first drop).

Unique tokens cannot ge merged.
Only tokens of the same event can be merged.

Here is some information about levels:
- level 0:
  - initial tokens of [FairXYZMH](./FairXYZMH.md) (first drop) collection
  - every event has 22 'editions'
  - powers of 2 tokens (2, 4, 8 or 16) can be merged to get high-level tokens (see `mergeBaseBatch`)
- level 1:
  - only 11 tokens of each event can be created
  - can be got from 2 tokens of 0th level
  - gives no reward
- level 2:
  - only 5 tokens of each event can be created
  - can be got from 4 tokens of 0th level or 2 tokens of 1st level
  - can give **reward token** from PROSPECT 100 collection (see [Prospect100](./Prospect100MH.md))
- level 3:
  - only 2 tokens of each event can be created
  - can be got from 8 tokens of 0th level or 2 tokens of 2nd level
  - can give **reward token** from PROSPECT 100 collection (see [Prospect100](./Prospect100MH.md))
- level 4:
  - only 1 token of each event can be created
  - can be got from 16 tokens of 0th level or 2 tokens of 3rd level
  - can give **reward token** from PROSPECT 100 collection (see [Prospect100](./Prospect100MH.md))

## Levels merging

<table>
    <thead>
        <tr>
            <th>Level 0</th>
            <th>Level 1</th>
            <th>Level 2</th>
            <th>Level 3</th>
            <th>Level 4</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=1>1 of 22</td>
            <td rowspan=2>1 of 11</td>
            <td rowspan=4>1 of 5</td>
            <td rowspan=8>1 of 2</td>
            <td rowspan=16>1 of 1</td>
        </tr>
        <tr>
            <td rowspan=1>2 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>3 of 22</td>
            <td rowspan=2>2 of 11</td>
        </tr>
        <tr>
            <td rowspan=1>4 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>5 of 22</td>
            <td rowspan=2>3 of 11</td>
            <td rowspan=4>2 of 5</td>
        </tr>
        <tr>
            <td rowspan=1>6 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>7 of 22</td>
            <td rowspan=2>4 of 11</td>
        </tr>
        <tr>
            <td rowspan=1>8 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>9 of 22</td>
            <td rowspan=2>5 of 11</td>
            <td rowspan=4>3 of 5</td>
            <td rowspan=8>2 of 2</td>
        </tr>
        <tr>
            <td rowspan=1>10 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>11 of 22</td>
            <td rowspan=2>6 of 11</td>
        </tr>
        <tr>
            <td rowspan=1>12 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>13 of 22</td>
            <td rowspan=2>7 of 11</td>
            <td rowspan=4>4 of 5</td>
        </tr>
        <tr>
            <td rowspan=1>14 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>15 of 22</td>
            <td rowspan=2>8 of 11</td>
        </tr>
        <tr>
            <td rowspan=1>16 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>17 of 22</td>
            <td rowspan=2>9 of 11</td>
            <td rowspan=4>5 of 5</td>
            <td rowspan=6>(reserve)</td>
            <td rowspan=6>(reserve)</td>
        </tr>
        <tr>
            <td rowspan=1>18 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>19 of 22</td>
            <td rowspan=2>10 of 11</td>
        </tr>
        <tr>
            <td rowspan=1>20 of 22</td>
        </tr>
        <tr>
            <td rowspan=1>21 of 22</td>
            <td rowspan=2>11 of 11</td>
            <td rowspan=2>(reserve)</td>
        </tr>
        <tr>
            <td rowspan=1>22 of 22</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <th>initial</th>
            <th>no rewards</th>
            <th>possible reward</th>
            <th>possible reward</th>
            <th>possible reward</th>
        </tr>
    </tfoot>
</table>

## Examples

### Base merge

Base merge is about merging initial tokens of [FairXYZMH](./FairXYZMH.md) (first drop) collection.

- token #5 and #104 can be merged (belongs to event #5) to get 1st level
- token #1 and #100 cannot be merged (token #1 is unique)
- token #5 and #6 cannot be merged (belongs to different events)
- token #5 and #5 cannot be merged (cannot merge token with self)
- token #5, #104, #203 and #302 can be merged (belongs to event #5) to get 2nd level
and **reward token** (if there are any unminted tokens of [Prospect100MH](./Prospect100MH.md))

### Advanced merge

Advanced merge is about merging tokens of 'high levels' of MergerMH (current collection)
- 1st level token of event #5 can be merged only with 1st level token of event #5
(also a **reward token** from Prospect100MH can be minted if there are still tokens left)
- 1st level token of event #5 cannot be merged with 1st level token of event #6 (different events)
- 1st level token of event #5 cannot be merged with 2nd level token of event #5 (different levels)
- actually any two tokens of the same event and same (n-th) level can be merged into one (n+1)-th level token
(and a **reward token** from Prospect100MH can be given if there are still reward tokens left)
