/* For license and copyright information please see the LEGAL file in the code repository */

package password_p

import (
	token_p "org/modules/computer/token/protocol"
)

// DataModel indicate the domain record data fields.
// A person can decide to don't register password and deny authenticate by password by relate the label.
type DataModel interface {
	token_p.Field_TokenID
	Field_PasswordHash
}
