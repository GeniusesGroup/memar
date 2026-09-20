//go:build lang_eng

/* For license and copyright information please see the LEGAL file in the code repository */

package errs

//memar:impl memar/protocol.Detail
func (d *badRequest) Domain() string  { return domainEnglish }
func (d *badRequest) Summary() string { return "Bad Request" }
func (d *badRequest) Overview() string {
	return "Some given data in request must be invalid or peer not accept them"
}
func (d *badRequest) UserNote() string { return "" }
func (d *badRequest) DevNote() string  { return "" }
func (d *badRequest) TAGS() []string   { return []string{} }

//memar:impl
func (d *badRequest) Name() string         { return "" }
func (d *badRequest) Abbreviation() string { return "" }
func (d *badRequest) Aliases() []string    { return []string{} }
