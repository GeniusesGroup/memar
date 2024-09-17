/* For license and copyright information please see the LEGAL file in the code repository */

package tp

import (
	up "org/modules/user/protocol"
)

// Serial numbers are identification numbers given to one product in particular,
// to allow to track the history of the item from reception to delivery and after-sales.
// e.g. https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity
type ThingUUID up.UserUUID
