//go:build cmd

/* For license and copyright information please see the LEGAL file in the code repository */
// Auto-generated, edits may be overwritten

package modules

import (
	cmd "memar/command"
	"memar/detail"
	"memar/mediatype"
	"memar/protocol"
	"memar/service"
)

var RootCommand rootCommand

type rootCommand struct {
	detail.DS
	mediatype.MT
	service.Service
	cmd.Command
}

// Init use to initialize all services and register them in the RootCommand.
func (rc *rootCommand) Init() {
	// project.Command.Init(rc)

	rc.Command.Init(nil, nil)
}

//memar:impl protocol.MediaType
func (s *rootCommand) FileExtension() string               { return "" }
func (s *rootCommand) Status() protocol.SoftwareStatus     { return protocol.Software_Unset }
func (s *rootCommand) ReferenceURI() string                { return "" }
func (s *rootCommand) IssueDate() protocol.Time            { return nil }
func (s *rootCommand) ExpiryDate() protocol.Time           { return nil }
func (s *rootCommand) ExpireInFavorOf() protocol.MediaType { return nil }

//memar:impl memar/protocol.Object
func (s *rootCommand) Fields() []protocol.Object_Member_Field   { return nil }
func (s *rootCommand) Methods() []protocol.Object_Member_Method { return nil }

//memar:impl protocol.Service
func (s *rootCommand) URI() string                 { return "" }
func (s *rootCommand) CRUDType() protocol.CRUD     { return protocol.CRUD_None }
func (s *rootCommand) UserType() protocol.UserType { return protocol.UserType_Unset }

//memar:impl protocol.OperationImportance
func (s *rootCommand) Priority() protocol.Priority { return protocol.Priority_Unset }
func (s *rootCommand) Weight() protocol.Weight     { return protocol.Weight_Unset }

//memar:impl protocol.ServiceDetails
func (s *rootCommand) Request() protocol.Object  { return nil }
func (s *rootCommand) Response() protocol.Object { return nil }

//memar:impl memar/protocol.Quiddity
func (s *rootCommand) Name() string         { return "organization" }
func (c *rootCommand) Abbreviation() string { return "org" }
func (s *rootCommand) Aliases() []string    { return []string{} }

//memar:impl protocol.Command
func (s *rootCommand) Runnable() bool { return false }

//memar:impl memar/protocol.CommandHandler
func (s *rootCommand) ServeCLA(arguments []string) (err protocol.Error) {
	err = cmd.ServeCLA(s, arguments)
	return
}
