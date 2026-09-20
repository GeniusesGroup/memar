/* For license and copyright information please see the LEGAL file in the code repository */

package answer_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_AnswerID interface {
	AnswerID() AnswerUUID
}

type AnswerUUID record_p.UUID
