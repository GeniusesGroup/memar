/* For license and copyright information please see the LEGAL file in the code repository */

package channel_p

import (
	// datatype_p "org/modules/computer/type/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

type Field_MetricUnit interface {
	// https://en.wikipedia.org/wiki/International_System_of_Units
	// Number, Gram, Liter, Second
	MetricUnit() label_p.UUID

	// TODO::: need above or use below??
	// datatype_p.Field_DataTypeID
}
