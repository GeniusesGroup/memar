/* For license and copyright information please see the LEGAL file in the code repository */

package org

/*
payto	Designate target for payments	Provisional

RFC 8905
https://datatracker.ietf.org/doc/html/rfc8905

payto://<authority>/<receiver>[?<options>]

examples:
payto://iban/DE75512108001245126199?amount=EUR:200.0&message=hello
payto://bic/SOGEDEFFXXX
payto://void/?amount=EUR:10.5
*/
