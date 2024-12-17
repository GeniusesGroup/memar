/* For license and copyright information please see the LEGAL file in the code repository */

package tcs_p

import (
	request_p "memar/audit/request/protocol"

	tc_p "org/modules/identity/thing-channel/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	tc_p.Field_ChannelID
	Field_Status

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
