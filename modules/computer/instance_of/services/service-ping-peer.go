/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/protocol"
	"memar/service"
)

var pingPeerService = service.Service{
	URN:                "domain/achaemenid.protocol.service; name=ping-peer",
	Domain:             DomainName,
	ID:                 6915176777280394057,
	IssueDate:          1595478242,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Ping Peer",
			Description: `Endpoints can use PING to verify that their peers are still alive or to check reachability to the peer.`,
			TAGS:        []string{},
		},
	},

	SRPCHandler: PingPeer,
}

// PingPeer : Endpoints can use PING to verify that their peers are still alive or to check reachability to the peer.
func PingPeer(st protocol.Stream) {
	// If the payload is not empty, the recipient MUST generate a PONG frame containing the same Data.
}

type pingPeerReq struct {
}
