# Pay
This bundle names the target of a money transfer with a `payto` URI, as specified by [RFC 8905](https://datatracker.ietf.org/doc/html/rfc8905).

## What it names
`payto://<authority>/<receiver>[?<options>]`

Recorded examples:

- `payto://iban/DE75512108001245126199?amount=EUR:200.0&message=hello`
- `payto://bic/SOGEDEFFXXX`
- `payto://void/?amount=EUR:10.5`

The provisional gloss on the scheme is: designate the target for payments.

## What it does not do
The account still holds the quantity. The transaction still moves it. This bundle is the name of the receiver, so a payer can point at an IBAN, a BIC, or a void target without this repository inventing a second transfer protocol.

## Open questions
- The note marks the scheme provisional. Which authorities this organization actually accepts (IBAN, BIC, void, others) is unset.
- Amount and message sit in the query string in the examples. Whether those are instructions to the transaction, or only a hint the payer shows, is unset.
