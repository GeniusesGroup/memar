/* For license and copyright information please see the LEGAL file in the code repository */

package takes_p

import (
	decimal_p "memar/math/decimal/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	decimal_p.Field_Quantity // + || -
}
