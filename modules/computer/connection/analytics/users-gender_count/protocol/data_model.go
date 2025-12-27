/* For license and copyright information please see the LEGAL file in the code repository */

package ugacp

import (
	ugp "org/modules/user-gender/protocol"
)

type DataModel interface {
	Gender() ugp.Gender
	Count() int64
}
