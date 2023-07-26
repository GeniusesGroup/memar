/* For license and copyright information please see the LEGAL file in the code repository */

package qmrp

import (
	"memar/protocol"

	op "org/modules/object/protocol"
)

type DataModel interface {
	ObjectID() op.ObjectUUID
	Rating() PictureRating_Rate

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

type PictureRating_Rate uint8

const (
// 0 : Suitable for display on all websites with any audience type.
// 1 : May contain rude gestures, provocatively dressed individuals, the lesser swear words, or mild violence.
// 2 : May contain such things as harsh profanity, intense violence, nudity, or hard drug use.
// 3 : May contain hardcore sexual imagery or extremely disturbing violence.
)
