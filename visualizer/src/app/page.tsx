


import { Graph } from './graph';
import { data } from "~/lib/data"

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b text-black bg-white">
      <link href='https://cdn.syncfusion.com/ej2/22.1.34/material.css' rel='stylesheet'></link>
      <Graph data={data} />
    </main>
  );
}
