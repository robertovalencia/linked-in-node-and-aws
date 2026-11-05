/** Credential-free runtime teaching examples; these are not application features. */
import assert from 'node:assert/strict';
import { EventEmitter, once } from 'node:events';
import { promises as fs, createReadStream, createWriteStream } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { pipeline } from 'node:stream/promises';
import { Writable } from 'node:stream';
import { AsyncLocalStorage } from 'node:async_hooks';
import { Worker } from 'node:worker_threads';
import { promisify } from 'node:util';
import { execFile } from 'node:child_process';
import { setTimeout as delay } from 'node:timers/promises';

const execute = promisify(execFile);
const passed = [];
const dir = await fs.mkdtemp(join(tmpdir(), 'node-runtime-lab-'));
try {
  const order = [];
  const emitter = new EventEmitter();
  emitter.on('example', () => order.push('listener'));
  order.push('before');
  emitter.emit('example');
  order.push('after');
  assert.deepEqual(order, ['before', 'listener', 'after']);
  assert.throws(() => new EventEmitter().emit('error', new Error('expected failure')), /expected failure/);
  passed.push('EventEmitter: synchronous order and unhandled error');

  // An ESM entry point is evaluated in an asynchronous module context.
  // These assertions compare only these small entry points, not every callback context.
  const schedule = `const out=['sync'];process.nextTick(()=>out.push('tick'));Promise.resolve().then(()=>out.push('promise'));setTimeout(()=>console.log(JSON.stringify(out)),20);`;
  const cjs = await execute(process.execPath, ['--input-type=commonjs', '-e', schedule]);
  const esm = await execute(process.execPath, ['--input-type=module', '-e', schedule]);
  assert.deepEqual(JSON.parse(cjs.stdout), ['sync', 'tick', 'promise']);
  assert.deepEqual(JSON.parse(esm.stdout), ['sync', 'promise', 'tick']);
  passed.push('Scheduling: CommonJS and ESM entry-point contexts');

  assert.equal('😀'.length, 2);
  assert.equal(Buffer.byteLength('😀'), 4);
  const counter = (() => { let value = 0; return () => ++value; })();
  assert.deepEqual([counter(), counter()], [1, 2]);
  const original = { skills: ['Node'] };
  const shallow = { ...original };
  shallow.skills.push('SQL');
  assert.deepEqual(original.skills, ['Node', 'SQL']);
  passed.push('Values: closure lifetime, shallow copy and encoded byte length');

  const source = join(dir, 'source');
  const target = join(dir, 'copy');
  await fs.writeFile(source, Buffer.alloc(200_000, 35));
  await pipeline(createReadStream(source), createWriteStream(target));
  const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');
  assert.equal(digest(await fs.readFile(source)), digest(await fs.readFile(target)));
  assert.equal((await fs.stat(target)).size, 200_000);
  const missingInput = createReadStream(join(dir, 'missing'));
  const failedOutput = createWriteStream(join(dir, 'failed'));
  const inputClosed = once(missingInput, 'close').catch(() => {});
  const outputClosed = once(failedOutput, 'close').catch(() => {});
  await assert.rejects(
    pipeline(missingInput, failedOutput),
    { code: 'ENOENT' },
  );
  await Promise.all([inputClosed, outputClosed]);
  assert.equal(missingInput.destroyed, true);
  assert.equal(failedOutput.destroyed, true);
  assert.equal(missingInput.closed, true);
  assert.equal(failedOutput.closed, true);
  passed.push('Pipeline: equal bytes, error rejection and both streams closed');

  let produced = 0;
  let consumed = 0;
  let drainWaits = 0;
  const sink = new Writable({
    highWaterMark: 16,
    write(chunk, encoding, complete) { consumed += 1; setTimeout(complete, 1); },
  });
  for (let i = 0; i < 100; i += 1) {
    produced += 1;
    if (!sink.write(Buffer.alloc(16))) {
      drainWaits += 1;
      await once(sink, 'drain');
    }
  }
  const finished = once(sink, 'finish');
  sink.end();
  await finished;
  assert.equal(produced, 100);
  assert.equal(consumed, produced);
  assert.ok(drainWaits > 0);
  passed.push('Backpressure: production pauses for drain; all 100 chunks consumed');

  const storage = new AsyncLocalStorage();
  const ids = await Promise.all(['one', 'two'].map((id, index) => storage.run(
    { requestId: id }, async () => {
      await delay(2 - index);
      return storage.getStore().requestId;
    },
  )));
  assert.deepEqual(ids, ['one', 'two']);
  passed.push('AsyncLocalStorage: overlapping runs keep separate IDs');

  const workerFile = join(dir, 'worker.mjs');
  await fs.writeFile(workerFile, "import { parentPort, workerData } from 'node:worker_threads'; parentPort.postMessage(workerData * workerData);\n");
  const worker = new Worker(pathToFileURL(workerFile), { workerData: 12, execArgv: [] });
  // Install both observers before either event can happen.
  const resultPromise = once(worker, 'message');
  const exitPromise = once(worker, 'exit');
  const [[result], [exitCode]] = await Promise.all([resultPromise, exitPromise]);
  assert.equal(result, 144);
  assert.equal(exitCode, 0);
  await fs.writeFile(workerFile, "throw new Error('expected worker failure');\n");
  const failingWorker = new Worker(pathToFileURL(workerFile), { execArgv: [] });
  const failedExit = new Promise((resolve) => failingWorker.once('exit', resolve));
  // Promise.all installs rejection handlers on both event promises immediately.
  await assert.rejects(Promise.all([
    once(failingWorker, 'message'), once(failingWorker, 'exit'),
  ]), /expected worker failure/);
  assert.notEqual(await failedExit, 0);
  passed.push('Worker: result 144, exit zero and failed worker rejection owned');

  const literal = 'value;$(this_is_literal)& space';
  const child = await execute(process.execPath, ['-e', 'console.log(process.argv[1])', literal]);
  assert.equal(child.stdout.trim(), literal);
  await assert.rejects(execute(process.execPath, ['-e', 'process.exitCode=7']), { code: 7 });
  passed.push('Child arguments: shell metacharacters remain literal; failure rejects');

  const signal = AbortSignal.timeout(5);
  await assert.rejects(delay(100, undefined, { signal }), { name: 'AbortError' });
  assert.equal(signal.aborted, true);
  assert.equal(signal.reason.name, 'TimeoutError');
  passed.push('Abort: timeout cancels a supported operation, with explicit failure');

  const query = new URLSearchParams({ q: 'Node & SQL' });
  assert.equal(new URLSearchParams(query.toString()).get('q'), 'Node & SQL');
  assert.equal(Number(''), 0);
  assert.equal(parseInt('12oops', 10), 12);
  passed.push('Input: URL query round-trip and numeric conversion edge cases');

  console.log(JSON.stringify({ node: process.version, passed: passed.length, checks: passed }, null, 2));
} finally {
  await fs.rm(dir, { recursive: true, force: true });
}
