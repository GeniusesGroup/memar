/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/authorization"
	"memar/protocol"
	"memar/service"
)

// CloseConnectionService store details about CloseConnection service
var CloseConnectionService = service.Service{
	URN:                "domain/achaemenid.protocol.service; name=close-connection",
	Domain:             DomainName,
	ID:                 9728831764117097852,
	IssueDate:          1595478242,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Close Connection",
			Description: `Close connection and drop all incomplete data & stream`,
			TAGS:        []string{},
		},
	},

	SRPCHandler: CloseConnection,
}

// CloseConnection close connection and drop all incomplete data & stream.
// Connection can be open again by use TransferConnection() if related service exist in platform!
func CloseConnection(st protocol.Stream) {
	protocol.App.Connections.CloseConnection(st.Connection)
}
