/* For license and copyright information please see the LEGAL file in the code repository */

package channel_p

import (
	request_p "memar/audit/request/protocol"

	storage_p "org/modules/storage/primitive/protocol"
)

type Service_Signal_Find_Request interface {
	Field_ChannelID
	storage_p.Pagination_Offset_Request
}

type Service_Signal_Find_Response interface {
	request_p.Field_RequestIDs
	storage_p.Pagination_Response
}
