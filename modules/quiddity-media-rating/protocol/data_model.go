/* For license and copyright information please see the LEGAL file in the code repository */

package qmrp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ObjectID() op.ObjectUUID        //
	Rating() PictureRating_Rate     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type PictureRating_Rate uint8

const (
// 0 : Suitable for display on all websites with any audience type.
// 1 : May contain rude gestures, provocatively dressed individuals, the lesser swear words, or mild violence.
// 2 : May contain such things as harsh profanity, intense violence, nudity, or hard drug use.
// 3 : May contain hardcore sexual imagery or extremely disturbing violence.
)
