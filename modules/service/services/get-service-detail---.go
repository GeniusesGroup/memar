/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"encoding/json"

	"memar/protocol"
)

// Service store needed data for a service to implement protocol.Service when embed to other struct that implements other methods!
type Service struct {
	uri    string // Fill just if any http like type handler needed! Simple URI not variabale included! API services can set like "/m?{{.ServiceID}}" but it is not efficient, find services by ID.
	status protocol.SoftwareStatus

	detail map[protocol.LanguageID]*ServiceDetail

	authorization Authorization
}

/*
*********** Service Encoders & Decoders ***********
 */

func (s *Service) FromSyllab() (err protocol.Error) {
	return
}

func (s *Service) ToSyllab() {
}

func (s *Service) LenOfSyllabStack() (ln uint32) {
	return
}

func (s *Service) LenOfSyllabHeap() (ln uint32) {
	return
}

func (s *Service) LenAsSyllab() uint64 {
	return uint64(s.LenOfSyllabStack() + s.LenOfSyllabHeap())
}

func (s *Service) jsonDecoder() (err protocol.Error) {
	json.Unmarshal(s.JSON, s)
	return
}

func (s *Service) ToJSON() {
	s.JSON, _ = json.Marshal(s)
}
