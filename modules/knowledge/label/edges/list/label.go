/* For license and copyright information please see the LEGAL file in the code repository */

package list

// [label, `list`, quiddity] >>

// Some usage example:
// - label (`Commodity` own by User(`Omid`)) `list` Product (abc)
// - label (`Suggestion` own by User(`Omid`)) `list` Task (123456)

// `label` is base on `quiddity`, so all quiddity level edges MUST be in mind
// `label` CAN be any user generated for any purpose:::
//
// ["MyGuitarPlayList", "Omid", "Owner"]
// Read in this model: label(MyGuitarPlayList) belong to user(Omid)
//
// ["MyGuitarPlayList", "Persia", "belongs_to_org"]
// Read in this model: label(MyGuitarPlayList) born in in org(Persia)
