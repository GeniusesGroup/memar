/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	label_p "org/modules/knowledge/label/protocol"
)

// Use to restrict the voucher on specific labels.
type Labels interface {
	Field_Each
	label_p.Field_LabelsUUID
}
