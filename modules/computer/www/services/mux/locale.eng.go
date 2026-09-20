//go:build lang_eng

/* For license and copyright information please see the LEGAL file in the code repository */

package hs

const domainEnglish = "HTTP Services"

func init() {
	MuxService.DS.SetDetail(lang_p.LanguageEnglish, domainEnglish,
		"Service Multiplexer",
		"Multiplex services by its ID with impressive performance",
		"",
		"",
		nil)
	HostSupportedService.DS.SetDetail(lang_p.LanguageEnglish, domainEnglish,
		"Host Supported",
		"Service to check if requested host is valid or not",
		"",
		"",
		nil)
}
