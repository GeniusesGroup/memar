/* For license and copyright information please see the LEGAL file in the code repository */

package ugacp

import (
	"memar/protocol"
	ugp "memar/modules/user-gender/protocol"
)

type DataModel interface {
	Gender() ugp.Gender
	Count() int64
}
