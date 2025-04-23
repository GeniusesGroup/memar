/* For license and copyright information please see the LEGAL file in the code repository */

package reference_p

import (
	label_p "org/modules/knowledge/label/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	// Store a label to indicate better relation reason
	// e.g. ChangedQuantityReason
	label_p.Field_LabelID
}
