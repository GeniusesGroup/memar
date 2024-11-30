/* For license and copyright information please see the LEGAL file in the code repository */

package law_p

import (
	request_p "memar/audit/request/protocol"

	language_p "org/modules/knowledge/language/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel give users the ability to vote to others and it allows them to make propositions on certain issues
type DataModel interface {
	Field_LawID
	language_p.Field_LanguageID // base language

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}

// TODO:::
// 	- If someone were to give their vote to another user not because they think that they are more knowledgeable on a subject
// 	  but because they received some sort of benefit, the election would lose purity
// 	- Normal elections allow citizens to keep their political preferences private whereas
// 	  LiquidFeedback demonstrates transparency when it comes to this in order to make sure users are who they say they are.
// 	- Schulze mathematical method: https://en.wikipedia.org/wiki/Schulze_method
// 	-
