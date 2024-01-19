"use client";

import { type Data } from '~/lib/data';
export function Graph({
  data,
}: {
  data: Data;
}) {

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b text-black bg-white">
     YO BRO
     {data[0].Close_BTC}
    </main>
  );
}
