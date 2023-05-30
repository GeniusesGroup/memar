/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type PictureRating interface {
	ObjectID() ObjectUUID           //
	Rating() PictureRating_Rate     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PictureRating_Rate uint8

const (
// 0 : Suitable for display on all websites with any audience type.
// 1 : May contain rude gestures, provocatively dressed individuals, the lesser swear words, or mild violence.
// 2 : May contain such things as harsh profanity, intense violence, nudity, or hard drug use.
// 3 : May contain hardcore sexual imagery or extremely disturbing violence.
)
