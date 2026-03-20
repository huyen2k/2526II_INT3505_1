import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service({
  title: "Library API - TypeSpec"
})
namespace Library;

model Book {
  id: int32;
  title: string;
  author: string;
}

model BookInput {
  title: string;
  author: string;
}

model ErrorResponse {
  error: string;
}

model MessageResponse {
  message: string;
}

model BooksResponse {
  data: Book[];
}

@route("/api/v1/books")
interface BooksCollection {
  @get op listBooks(): BooksResponse;
  @post op createBook(@body body: BookInput): Book | ErrorResponse;
}

@route("/api/v1/books/{book_id}")
interface BooksItem {
  @get op getBook(@path book_id: int32): Book | ErrorResponse;
  @put op updateBook(@path book_id: int32, @body body: BookInput): Book | ErrorResponse;
  @delete op deleteBook(@path book_id: int32): MessageResponse | ErrorResponse;
}
